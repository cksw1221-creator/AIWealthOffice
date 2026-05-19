"""Helpers for polling Multica issue progress."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .client import redact


def _as_list(payload: Any) -> list[Any]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, Sequence) and not isinstance(payload, (str, bytes, bytearray)):
        return list(payload)
    return []


def _select_latest_run(runs: Sequence[Mapping[str, Any]]) -> Mapping[str, Any] | None:
    if not runs:
        return None
    return sorted(
        runs,
        key=lambda run: (
            str(run.get("started_at") or ""),
            int(run.get("attempt") or 0),
            str(run.get("id") or ""),
        ),
    )[-1]


def _message_preview(message: Mapping[str, Any]) -> str:
    if "content" in message:
        return str(message["content"]).strip()
    if "output" in message:
        return str(redact(message["output"])).strip()
    if "input" in message:
        return str(redact(message["input"])).strip()
    return ""


def poll_issue(client: Any, issue_id: str, *, since_seq: int | None = None) -> dict[str, Any]:
    issue_result = client.issue_get(issue_id)
    runs_result = client.issue_runs(issue_id)
    if not issue_result.ok:
        raise RuntimeError(issue_result.stderr or issue_result.stdout)
    if not runs_result.ok:
        raise RuntimeError(runs_result.stderr or runs_result.stdout)

    issue = issue_result.parsed if isinstance(issue_result.parsed, dict) else {}
    runs = [run for run in _as_list(runs_result.parsed) if isinstance(run, Mapping)]
    latest_run = _select_latest_run(runs)

    messages: list[Mapping[str, Any]] = []
    if latest_run and latest_run.get("id"):
        messages_result = client.issue_run_messages(
            str(latest_run["id"]),
            issue_id=issue_id,
            since=since_seq,
        )
        if not messages_result.ok:
            raise RuntimeError(messages_result.stderr or messages_result.stdout)
        messages = [item for item in _as_list(messages_result.parsed) if isinstance(item, Mapping)]

    last_message = None
    if messages:
        raw = messages[-1]
        last_message = {
            "seq": raw.get("seq"),
            "type": raw.get("type"),
            "preview": _message_preview(raw),
        }

    return {
        "issue": redact(issue),
        "runs": redact(list(runs)),
        "latest_run": redact(dict(latest_run)) if latest_run else None,
        "messages": redact(list(messages)),
        "last_message": redact(last_message),
    }


def format_issue_summary(summary: Mapping[str, Any]) -> str:
    issue = summary.get("issue") if isinstance(summary.get("issue"), Mapping) else {}
    latest_run = summary.get("latest_run") if isinstance(summary.get("latest_run"), Mapping) else {}
    last_message = summary.get("last_message") if isinstance(summary.get("last_message"), Mapping) else {}

    identifier = issue.get("identifier") or issue.get("id") or "<unknown>"
    title = issue.get("title") or "<untitled>"
    status = issue.get("status") or "<unknown>"
    lines = [
        f"Issue {identifier}: {title}",
        f"Status: {status}",
    ]

    if latest_run:
        lines.append(
            "Latest run: "
            f"{latest_run.get('status', '<unknown>')} "
            f"(run {latest_run.get('id', '<unknown>')}, attempt {latest_run.get('attempt', '?')})"
        )
    else:
        lines.append("Latest run: none")

    if last_message:
        lines.append(
            f"Last message #{last_message.get('seq', '?')} ({last_message.get('type', 'unknown')}): "
            f"{last_message.get('preview', '')}"
        )
    else:
        lines.append("Last message: none")

    return "\n".join(lines)
