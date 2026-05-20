from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES_PATH = Path("workspace") / "closure_sync_rules.json"
DEFAULT_PROJECT_METADATA_PATH = Path("workspace") / "project_sprint_metadata.json"
DEFAULT_DEMO_REGISTRY_PATH = Path("workspace") / "demo_registry.json"

OPEN_STATES = {"backlog", "todo", "in_progress", "in_review"}
DONE_STATES = {"done", "completed"}


def apply_local_closure_sync(
    *,
    issue_key: str,
    title: str,
    status: str,
    repo_root: str | Path = REPO_ROOT,
    rules_path: str | Path = DEFAULT_RULES_PATH,
    project_metadata_path: str | Path = DEFAULT_PROJECT_METADATA_PATH,
    demo_registry_path: str | Path = DEFAULT_DEMO_REGISTRY_PATH,
) -> dict[str, Any]:
    root = Path(repo_root)
    normalized_status = status.strip().lower()
    if normalized_status not in DONE_STATES:
        return {
            "applied": False,
            "reason": f"status '{status}' is not a closure state",
            "project_metadata": {"updated": False},
            "demo_registry": {"updated": False},
        }

    project_result = sync_project_metadata(
        issue_key=issue_key,
        title=title,
        repo_root=root,
        metadata_path=project_metadata_path,
    )
    registry_result = sync_demo_registry(
        issue_key=issue_key,
        title=title,
        repo_root=root,
        rules_path=rules_path,
        registry_path=demo_registry_path,
    )
    return {
        "applied": project_result.get("updated", False) or registry_result.get("updated", False),
        "project_metadata": project_result,
        "demo_registry": registry_result,
    }


def sync_project_metadata(
    *,
    issue_key: str,
    title: str,
    repo_root: Path,
    metadata_path: str | Path,
) -> dict[str, Any]:
    path = repo_root / Path(metadata_path)
    if not path.exists():
        return {"updated": False, "reason": "project metadata file missing"}

    payload = json.loads(path.read_text(encoding="utf-8"))
    projects = payload.get("projects", {})
    changed_projects: list[str] = []

    for project_name, project in projects.items():
        activation_order = project.get("activation_order")
        if not isinstance(activation_order, list):
            continue

        matched = False
        for entry in activation_order:
            if not isinstance(entry, dict):
                continue
            if entry.get("issue") == issue_key or entry.get("title") == title:
                entry["status"] = "done"
                matched = True

        if not matched:
            continue

        open_entries = [entry for entry in activation_order if str(entry.get("status", "")).lower() in OPEN_STATES]
        done_entries = [entry for entry in activation_order if str(entry.get("status", "")).lower() in DONE_STATES]
        project["done_count"] = len(done_entries)
        project["issue_count"] = len(activation_order)
        if open_entries:
            project["current_entry_issue"] = open_entries[0].get("issue")
            project["status"] = "in_progress"
        else:
            project["current_entry_issue"] = None
            project["status"] = "completed"
        project["notes"] = f"Last accepted issue: {issue_key} — {title}"
        changed_projects.append(project_name)

    if not changed_projects:
        return {"updated": False, "reason": "no matching activation entry found"}

    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"updated": True, "projects": changed_projects}


def sync_demo_registry(
    *,
    issue_key: str,
    title: str,
    repo_root: Path,
    rules_path: str | Path,
    registry_path: str | Path,
) -> dict[str, Any]:
    rules_file = repo_root / Path(rules_path)
    registry_file = repo_root / Path(registry_path)
    if not rules_file.exists():
        return {"updated": False, "reason": "closure sync rules file missing"}
    if not registry_file.exists():
        return {"updated": False, "reason": "demo registry file missing"}

    rules_payload = json.loads(rules_file.read_text(encoding="utf-8"))
    registry_payload = json.loads(registry_file.read_text(encoding="utf-8"))
    demos = registry_payload.setdefault("demos", {})
    changed_demo_ids: list[str] = []

    for rule in rules_payload.get("rules", []):
        if not isinstance(rule, dict):
            continue
        match = rule.get("match", {})
        match_issue = match.get("issue_key")
        match_title = match.get("title")
        if match_issue and match_issue != issue_key:
            continue
        if match_title and match_title != title:
            continue

        demo_id = rule.get("demo_id")
        demo_record = rule.get("demo_record")
        if not demo_id or not isinstance(demo_record, dict):
            continue

        applied_record = _materialize_demo_record(demo_record)
        demos[demo_id] = applied_record
        changed_demo_ids.append(str(demo_id))

    if not changed_demo_ids:
        return {"updated": False, "reason": "no matching demo rule found"}

    registry_file.write_text(json.dumps(registry_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"updated": True, "demo_ids": changed_demo_ids}


def _materialize_demo_record(record: dict[str, Any]) -> dict[str, Any]:
    cloned = json.loads(json.dumps(record))
    accepted_date = cloned.get("accepted_date")
    if accepted_date == "__TODAY__":
        cloned["accepted_date"] = date.today().isoformat()
    return cloned