"""Helpers for CEO-facing Multica workflows."""

from __future__ import annotations

import json
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .client import MulticaClient


DEFAULT_REGISTRY_PATH = Path("workspace") / "worker_registry.json"
DEFAULT_CONTINUITY_PATH = Path("workspace") / "session_continuity.json"
SESSION_MODES = ("fresh", "resume", "fork", "force-fresh")


def load_worker_registry(path: str | Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    registry_path = Path(path)
    return json.loads(registry_path.read_text(encoding="utf-8"))


def normalize_session_mode(session_mode: str) -> str:
    normalized = session_mode.strip().lower()
    if normalized not in SESSION_MODES:
        allowed = ", ".join(SESSION_MODES)
        raise ValueError(f"Unsupported session mode '{session_mode}'. Expected one of: {allowed}.")
    return normalized


def load_session_continuity(path: str | Path = DEFAULT_CONTINUITY_PATH) -> dict[str, Any]:
    continuity_path = Path(path)
    if not continuity_path.exists():
        return {"issues": {}}
    payload = json.loads(continuity_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {"issues": {}}
    issues = payload.get("issues")
    if not isinstance(issues, dict):
        payload["issues"] = {}
    return payload


def save_session_continuity(payload: Mapping[str, Any], path: str | Path = DEFAULT_CONTINUITY_PATH) -> None:
    continuity_path = Path(path)
    continuity_path.parent.mkdir(parents=True, exist_ok=True)
    continuity_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _ensure_issue_entry(
    store: dict[str, Any],
    *,
    issue_storage_id: str,
    issue_id: str,
    issue_key: str,
    title: str,
) -> dict[str, Any]:
    issues = store.setdefault("issues", {})
    entry = issues.get(issue_storage_id)
    if not isinstance(entry, dict):
        entry = {"issue_id": issue_id, "issue_key": issue_key, "title": title}
        issues[issue_storage_id] = entry
    entry["issue_id"] = issue_id
    entry["issue_key"] = issue_key
    entry["title"] = title
    return entry


def record_dispatch_continuity(
    *,
    issue_id: str,
    issue_key: str,
    title: str,
    worker: Mapping[str, Any],
    status: str | None,
    priority: str | None,
    session_mode: str,
    continuity_path: str | Path = DEFAULT_CONTINUITY_PATH,
) -> None:
    normalized = normalize_session_mode(session_mode)
    store = load_session_continuity(continuity_path)
    entry = _ensure_issue_entry(
        store,
        issue_storage_id=issue_id,
        issue_id=issue_id,
        issue_key=issue_key,
        title=title,
    )
    entry["worker"] = {
        "name": str(worker.get("name", "")),
        "agent_id": str(worker.get("agent_id", "")),
        "role": str(worker.get("role", "")),
    }
    entry["dispatch"] = {
        "priority": priority,
        "status": status,
    }
    entry["continuity"] = {
        "recommended_mode": normalized,
        "last_action": "dispatch",
    }
    save_session_continuity(store, continuity_path)


def record_review_continuity(
    *,
    issue_id: str,
    comment: str,
    status: str,
    session_mode: str,
    continuity_path: str | Path = DEFAULT_CONTINUITY_PATH,
) -> None:
    normalized = normalize_session_mode(session_mode)
    store = load_session_continuity(continuity_path)
    entry = _ensure_issue_entry(
        store,
        issue_storage_id=issue_id,
        issue_id=issue_id,
        issue_key=issue_id,
        title=str(store.get("issues", {}).get(issue_id, {}).get("title", issue_id)),
    )
    entry["review"] = {
        "status": status,
        "comment_preview": comment.strip(),
    }
    entry["continuity"] = {
        "recommended_mode": normalized,
        "last_action": "review",
    }
    save_session_continuity(store, continuity_path)


def resolve_worker(registry: Mapping[str, Any], worker_ref: str) -> dict[str, Any]:
    workers = registry.get("workers")
    if not isinstance(workers, Mapping):
        raise ValueError("Worker registry is missing a 'workers' mapping.")

    for name, details in workers.items():
        if not isinstance(details, Mapping):
            continue
        if worker_ref == name or worker_ref == str(details.get("agent_id")):
            return {"name": str(name), **details}
    raise ValueError(f"Worker '{worker_ref}' was not found in the registry.")


def read_text_input(
    *,
    text: str | None = None,
    file_path: str | Path | None = None,
    use_stdin: bool = False,
) -> str:
    provided = sum(value is not None and value != "" for value in (text, file_path)) + int(use_stdin)
    if provided != 1:
        raise ValueError("Provide exactly one of text, file_path, or use_stdin.")
    if text is not None:
        return text
    if file_path is not None:
        return Path(file_path).read_text(encoding="utf-8")
    import sys

    return sys.stdin.read()


def _write_utf8_temp_file(content: str) -> tempfile.NamedTemporaryFile[str]:
    temp_file = tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".md")
    temp_file.write(content)
    temp_file.flush()
    temp_file.close()
    return temp_file


def _parsed_or_raise(result: Any, action: str) -> dict[str, Any]:
    if not result.ok:
        raise RuntimeError(f"{action} failed: {result.stderr or result.stdout}".strip())
    if isinstance(result.parsed, dict):
        return result.parsed
    raise RuntimeError(f"{action} did not return a JSON object.")


def dispatch_issue(
    client: MulticaClient,
    *,
    title: str,
    description: str,
    worker_ref: str,
    registry_path: str | Path = DEFAULT_REGISTRY_PATH,
    continuity_path: str | Path = DEFAULT_CONTINUITY_PATH,
    priority: str | None = None,
    status: str | None = None,
    session_mode: str = "fresh",
) -> dict[str, Any]:
    registry = load_worker_registry(registry_path)
    worker = resolve_worker(registry, worker_ref)
    normalized_session_mode = normalize_session_mode(session_mode)

    temp_file = _write_utf8_temp_file(description)
    try:
        result = client.issue_create(
            title,
            description_file=temp_file.name,
            priority=priority,
            status=status,
            assignee_id=str(worker["agent_id"]),
        )
    finally:
        Path(temp_file.name).unlink(missing_ok=True)

    payload = _parsed_or_raise(result, "Issue creation")
    payload["assignee_id"] = str(worker["agent_id"])
    payload["assignee_name"] = worker["name"]
    payload["session_mode"] = normalized_session_mode
    record_dispatch_continuity(
        issue_id=str(payload.get("id", "")),
        issue_key=str(payload.get("identifier", payload.get("id", ""))),
        title=title,
        worker=worker,
        status=status,
        priority=priority,
        session_mode=normalized_session_mode,
        continuity_path=continuity_path,
    )
    return payload


def review_issue(
    client: MulticaClient,
    *,
    issue_id: str,
    comment: str,
    status: str,
    continuity_path: str | Path = DEFAULT_CONTINUITY_PATH,
    session_mode: str = "resume",
) -> dict[str, Any]:
    normalized_session_mode = normalize_session_mode(session_mode)
    temp_file = _write_utf8_temp_file(comment)
    try:
        comment_result = client.issue_comment_add(issue_id, content_file=temp_file.name)
    finally:
        Path(temp_file.name).unlink(missing_ok=True)

    status_result = client.issue_status(issue_id, status)
    record_review_continuity(
        issue_id=issue_id,
        comment=comment,
        status=status,
        session_mode=normalized_session_mode,
        continuity_path=continuity_path,
    )
    return {
        "comment": _parsed_or_raise(comment_result, "Issue comment"),
        "status": _parsed_or_raise(status_result, "Issue status update"),
        "session_mode": normalized_session_mode,
    }
