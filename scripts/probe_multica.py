from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ga_multica import CapabilityCheck, MulticaClient, redact


MATRIX_PATH = ROOT / "workspace" / "multica_capability_matrix.json"
REPORT_PATH = ROOT / "reports" / "environment_report.md"


def summarize(value: Any) -> str:
    if isinstance(value, list):
        return f"{len(value)} item(s)"
    if isinstance(value, dict):
        for key in ("items", "data", "results", "workspaces", "agents", "runtimes", "issues"):
            item = value.get(key)
            if isinstance(item, list):
                return f"{len(item)} item(s) in {key}"
        return f"object with {len(value)} field(s)"
    if value is None:
        return "no JSON payload"
    return type(value).__name__


def first_list(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for item in payload.values():
            if isinstance(item, list):
                return item
    return []


def text_preview(text: str, *, limit: int = 600) -> str:
    compact = "\n".join(line.rstrip() for line in text.strip().splitlines() if line.strip())
    return compact[:limit] + ("..." if len(compact) > limit else "")


def record(name: str, output_kind: str, result: Any) -> CapabilityCheck:
    parsed = result.parsed
    text_output = result.stdout or result.stderr
    output = parsed if parsed is not None else text_preview(text_output)
    return CapabilityCheck(
        name=name,
        command=tuple(result.args),
        ok=result.ok,
        returncode=result.returncode,
        output_kind=output_kind,  # type: ignore[arg-type]
        timed_out=result.timed_out,
        summary=summarize(parsed) if parsed is not None else text_preview(text_output, limit=180),
        data=redact(output),
        error=text_preview(result.stderr, limit=300) if result.stderr and not result.ok else None,
    )


def find_workspace_id(workspace_result: Any) -> str | None:
    env_id = os.environ.get("MULTICA_WORKSPACE_ID")
    if env_id:
        return env_id
    for row in first_list(workspace_result.parsed):
        if isinstance(row, dict):
            for key in ("id", "workspace_id", "workspaceId"):
                if row.get(key):
                    return str(row[key])
    return None


def names_from_payload(payload: Any) -> list[str]:
    names: list[str] = []
    for row in first_list(payload):
        if isinstance(row, dict):
            names.append(str(row.get("name") or row.get("title") or row.get("id") or "<unnamed>"))
        else:
            names.append(str(row))
    return names


def write_report(matrix: dict[str, Any]) -> None:
    checks = {item["name"]: item for item in matrix["capabilities"]}
    runtimes = names_from_payload(checks.get("runtime_list", {}).get("data"))
    agents = names_from_payload(checks.get("agent_list", {}).get("data"))
    lines = [
        "# Multica Environment Report",
        "",
        f"Generated: {matrix['generated_at']}",
        f"CLI path: `{matrix['cli']['path']}`",
        f"CLI version: `{matrix['cli']['version']}`",
        f"Auth status: {checks.get('auth_status', {}).get('summary', 'unknown')}",
        f"Workspace ID: `{matrix.get('workspace_id') or 'not detected from table output'}`",
        "",
        "## Capability Matrix",
        "",
        "| Capability | OK | Output | Summary |",
        "| --- | --- | --- | --- |",
    ]
    for item in matrix["capabilities"]:
        summary = str(item.get("summary") or "").replace("|", "/").replace("\n", "<br>")
        lines.append(
            f"| {item['name']} | {'yes' if item['ok'] else 'no'} | {item['output_kind']} | "
            f"{summary} |"
        )
    lines.extend([
        "",
        "## Runtimes",
        "",
        *(f"- {name}" for name in (runtimes or ["none returned"])),
        "",
        "## Agents",
        "",
        *(f"- {name}" for name in (agents or ["none returned"])),
        "",
        "## Redaction",
        "",
        "- Token-like fields and bearer values are redacted before writing outputs.",
        "- Probe does not read `.env`, key, or PEM files.",
    ])
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    client = MulticaClient(timeout_seconds=25)
    MATRIX_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    version = client.version()
    auth = client.auth_status()
    workspaces = client.workspace_list()
    workspace_id = find_workspace_id(workspaces)
    workspace_client = MulticaClient(timeout_seconds=25, workspace_id=workspace_id)

    checks = [
        record("version", "json", version),
        record("auth_status", "table", auth),
        record("workspace_list", "table", workspaces),
        record("runtime_list", "json", workspace_client.runtime_list()),
        record("agent_list", "json", workspace_client.agent_list()),
        record("issue_list", "json", workspace_client.issue_list(limit=10)),
        CapabilityCheck(
            name="issue_create",
            command=(client.executable, "issue", "create", "--output", "json", "--title", "<title>"),
            ok=True,
            returncode=0,
            output_kind="json",
            summary="available in adapter; skipped to avoid creating a probe issue",
        ),
    ]

    issue_id = None
    issues_payload = checks[5].data
    for issue in first_list(issues_payload):
        if isinstance(issue, dict) and issue.get("id"):
            issue_id = str(issue["id"])
            break
    if issue_id:
        checks.append(record("issue_get", "json", workspace_client.issue_get(issue_id)))
        runs = workspace_client.issue_runs(issue_id)
        checks.append(record("issue_runs", "json", runs))
        task_id = None
        for run in first_list(runs.parsed):
            if isinstance(run, dict) and run.get("id"):
                task_id = str(run["id"])
                break
        if task_id:
            checks.append(record("issue_run_messages", "json", workspace_client.issue_run_messages(task_id, issue_id=issue_id)))
        else:
            checks.append(
                CapabilityCheck(
                    name="issue_run_messages",
                    command=(client.executable, "issue", "run-messages", "<task-id>", "--output", "json"),
                    ok=False,
                    returncode=0,
                    output_kind="json",
                    summary="skipped: no issue runs returned",
                )
            )
    else:
        checks.extend([
            CapabilityCheck(
                name="issue_get",
                command=(client.executable, "issue", "get", "<issue-id>", "--output", "json"),
                ok=False,
                returncode=0,
                output_kind="json",
                summary="skipped: no issues returned",
            ),
            CapabilityCheck(
                name="issue_runs",
                command=(client.executable, "issue", "runs", "<issue-id>", "--output", "json"),
                ok=False,
                returncode=0,
                output_kind="json",
                summary="skipped: no issues returned",
            ),
            CapabilityCheck(
                name="issue_run_messages",
                command=(client.executable, "issue", "run-messages", "<task-id>", "--output", "json"),
                ok=False,
                returncode=0,
                output_kind="json",
                summary="skipped: no issues returned",
            ),
        ])

    matrix = {
        "generated_at": datetime.now(UTC).isoformat(),
        "cli": {
            "path": client.executable_path,
            "version": version.parsed or text_preview(version.stdout),
        },
        "workspace_id": workspace_id,
        "capabilities": [asdict(check) for check in checks],
    }
    matrix = redact(matrix)
    MATRIX_PATH.write_text(json.dumps(matrix, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_report(matrix)

    failed = [check.name for check in checks if not check.ok and not str(check.summary).startswith("skipped:")]
    if failed:
        print(f"Probe completed with failed capabilities: {', '.join(failed)}")
        return 1
    print(f"Wrote {MATRIX_PATH.relative_to(ROOT)} and {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
