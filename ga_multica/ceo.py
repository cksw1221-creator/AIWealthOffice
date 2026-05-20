"""Helpers for CEO-facing Multica workflows."""

from __future__ import annotations

import json
import tempfile
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .closure_sync import apply_local_closure_sync
from .client import MulticaClient


DEFAULT_REGISTRY_PATH = Path("workspace") / "worker_registry.json"
DEFAULT_CONTINUITY_PATH = Path("workspace") / "session_continuity.json"
DEFAULT_CLOSURE_MANIFEST_PATH = Path("workspace") / "closure_manifest.json"
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


def load_closure_manifest(path: str | Path = DEFAULT_CLOSURE_MANIFEST_PATH) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.exists():
        return {"issues": {}}
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return {"issues": {}}
    issues = payload.get("issues")
    if not isinstance(issues, dict):
        payload["issues"] = {}
    return payload


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


def _replace_once(text: str, search: str, replace: str, *, file_path: Path) -> str:
    if search not in text:
        raise ValueError(f"Expected to find '{search}' in {file_path.as_posix()} before closure update.")
    return text.replace(search, replace, 1)


def _apply_gap_list_updates(repo_root: Path, updates: list[Mapping[str, Any]]) -> list[str]:
    file_path = repo_root / "workspace" / "current_gap_list.md"
    content = file_path.read_text(encoding="utf-8")
    changed = False
    for update in updates:
        search = str(update.get("search", ""))
        replace = str(update.get("replace", ""))
        if not search:
            raise ValueError("Gap list closure updates require a non-empty 'search' field.")
        new_content = _replace_once(content, search, replace, file_path=file_path)
        changed = changed or new_content != content
        content = new_content
    if changed:
        file_path.write_text(content, encoding="utf-8")
        return [file_path.as_posix()]
    return []


def _apply_project_metadata_updates(repo_root: Path, updates: list[Mapping[str, Any]]) -> list[str]:
    file_path = repo_root / "workspace" / "project_sprint_metadata.json"
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    projects = payload.get("projects")
    if not isinstance(projects, dict):
        raise ValueError("Project metadata file is missing a 'projects' object.")

    changed = False
    for update in updates:
        project_name = str(update.get("project", ""))
        if not project_name:
            raise ValueError("Project metadata closure updates require a 'project' field.")
        project = projects.get(project_name)
        if not isinstance(project, dict):
            raise ValueError(f"Project '{project_name}' was not found in project metadata.")

        if "current_entry_issue" in update:
            project["current_entry_issue"] = str(update["current_entry_issue"])
            changed = True

        append_notes = update.get("append_notes")
        if append_notes:
            note_text = str(append_notes)
            existing_notes = str(project.get("notes", ""))
            if note_text not in existing_notes:
                project["notes"] = f"{existing_notes} {note_text}".strip()
                changed = True

    if changed:
        file_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return [file_path.as_posix()]
    return []


def _apply_demo_registry_updates(
    repo_root: Path,
    issue_id: str,
    status: str,
    updates: Mapping[str, Any],
) -> list[str]:
    file_path = repo_root / "workspace" / "demo_registry.json"
    payload = json.loads(file_path.read_text(encoding="utf-8"))
    demos = payload.setdefault("demos", {})
    if not isinstance(demos, dict):
        raise ValueError("Demo registry file is missing a 'demos' object.")

    changed = False
    for demo_id, record in updates.items():
        if not isinstance(record, Mapping):
            raise ValueError(f"Demo registry update for '{demo_id}' must be an object.")
        merged = dict(demos.get(demo_id, {})) if isinstance(demos.get(demo_id), Mapping) else {}
        merged.update(record)
        merged.setdefault("id", demo_id)
        merged["accepted_issue"] = issue_id
        merged["accepted_status"] = status
        demos[demo_id] = merged
        changed = True

    if changed:
        file_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return [file_path.as_posix()]
    return []


def apply_closure_updates(
    *,
    issue_id: str,
    status: str,
    repo_root: str | Path,
    closure_manifest_path: str | Path = DEFAULT_CLOSURE_MANIFEST_PATH,
) -> list[str]:
    manifest = load_closure_manifest(closure_manifest_path)
    issue_updates = manifest.get("issues", {}).get(issue_id)
    if not isinstance(issue_updates, Mapping):
        return []

    apply_on_status = issue_updates.get("apply_on_status", [])
    normalized_statuses = {str(value) for value in apply_on_status if str(value)}
    if normalized_statuses and status not in normalized_statuses:
        return []

    repo_root_path = Path(repo_root)
    changed_files: list[str] = []

    demo_updates = issue_updates.get("demo_registry_updates")
    if isinstance(demo_updates, Mapping):
        changed_files.extend(_apply_demo_registry_updates(repo_root_path, issue_id, status, demo_updates))

    project_updates = issue_updates.get("project_metadata_updates")
    if isinstance(project_updates, list):
        changed_files.extend(_apply_project_metadata_updates(repo_root_path, project_updates))

    gap_updates = issue_updates.get("gap_list_updates")
    if isinstance(gap_updates, list):
        changed_files.extend(_apply_gap_list_updates(repo_root_path, gap_updates))

    return changed_files


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
    repo_root: str | Path = ".",
    closure_manifest_path: str | Path = DEFAULT_CLOSURE_MANIFEST_PATH,
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
    changed_files = apply_closure_updates(
        issue_id=issue_id,
        status=status,
        repo_root=repo_root,
        closure_manifest_path=closure_manifest_path,
    )
    return {
        "comment": _parsed_or_raise(comment_result, "Issue comment"),
        "status": _parsed_or_raise(status_result, "Issue status update"),
        "session_mode": normalized_session_mode,
        "closure_updates": changed_files,
    }
