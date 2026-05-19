"""Helpers for CEO-facing Multica workflows."""

from __future__ import annotations

import json
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .client import MulticaClient


DEFAULT_REGISTRY_PATH = Path("workspace") / "worker_registry.json"


def load_worker_registry(path: str | Path = DEFAULT_REGISTRY_PATH) -> dict[str, Any]:
    registry_path = Path(path)
    return json.loads(registry_path.read_text(encoding="utf-8"))


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
    priority: str | None = None,
    status: str | None = None,
) -> dict[str, Any]:
    registry = load_worker_registry(registry_path)
    worker = resolve_worker(registry, worker_ref)

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
    return payload


def review_issue(
    client: MulticaClient,
    *,
    issue_id: str,
    comment: str,
    status: str,
) -> dict[str, Any]:
    temp_file = _write_utf8_temp_file(comment)
    try:
        comment_result = client.issue_comment_add(issue_id, content_file=temp_file.name)
    finally:
        Path(temp_file.name).unlink(missing_ok=True)

    status_result = client.issue_status(issue_id, status)
    return {
        "comment": _parsed_or_raise(comment_result, "Issue comment"),
        "status": _parsed_or_raise(status_result, "Issue status update"),
    }
