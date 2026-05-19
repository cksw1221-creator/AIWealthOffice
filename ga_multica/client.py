"""Small, safe wrapper around the local ``multica`` CLI."""

from __future__ import annotations

import os
import json
import re
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .models import CommandResult, OutputKind


SECRET_PATTERNS = (
    re.compile(r"(?i)(token|secret|password|api[_-]?key)(\s*[:=]\s*)([^\s,;]+)"),
    re.compile(r"(?i)(bearer\s+)[a-z0-9._~+/=-]+"),
)


def redact(value: Any) -> Any:
    """Redact likely credentials from nested CLI output."""

    if isinstance(value, str):
        redacted = value
        for pattern in SECRET_PATTERNS:
            if pattern.groups >= 3:
                redacted = pattern.sub(r"\1\2[REDACTED]", redacted)
            else:
                redacted = pattern.sub(r"\1[REDACTED]", redacted)
        return redacted
    if isinstance(value, list):
        return [redact(item) for item in value]
    if isinstance(value, tuple):
        return tuple(redact(item) for item in value)
    if isinstance(value, Mapping):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if re.search(r"(?i)(token|secret|password|api[_-]?key)", key_text):
                cleaned[key_text] = "[REDACTED]"
            else:
                cleaned[key_text] = redact(item)
        return cleaned
    return value


def resolve_multica_executable(executable: str | Path = "multica") -> str:
    """Resolve the Multica CLI even when the current process PATH is stale."""

    text = str(executable)
    explicit = Path(text).expanduser()
    if explicit.exists():
        return str(explicit)

    env_path = os.environ.get("MULTICA_CLI")
    if env_path and Path(env_path).expanduser().exists():
        return str(Path(env_path).expanduser())

    found = shutil.which(text)
    if found:
        return found

    home = Path.home()
    candidates = [
        home / ".multica" / "bin" / "multica.exe",
        home / ".multica" / "bin" / "multica",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return text


class MulticaClient:
    """Typed convenience methods for supported Multica CLI commands."""

    def __init__(
        self,
        executable: str | Path = "multica",
        *,
        timeout_seconds: int = 20,
        workspace_id: str | None = None,
    ) -> None:
        self.executable = str(executable)
        self.timeout_seconds = timeout_seconds
        self.workspace_id = workspace_id

    @property
    def executable_path(self) -> str:
        return resolve_multica_executable(self.executable)

    def run(
        self,
        args: Sequence[str],
        *,
        output: OutputKind = "json",
        timeout_seconds: int | None = None,
    ) -> CommandResult:
        command = [self.executable_path, *args]
        if self.workspace_id:
            command.extend(["--workspace-id", self.workspace_id])

        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                check=False,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds or self.timeout_seconds,
            )
        except subprocess.TimeoutExpired as exc:
            return CommandResult(
                args=tuple(command),
                returncode=124,
                stdout=redact(exc.stdout or ""),
                stderr=redact(exc.stderr or f"Timed out after {exc.timeout} seconds"),
                timed_out=True,
            )

        stdout = redact(completed.stdout or "")
        stderr = redact(completed.stderr or "")
        parsed: Any | None = None
        if output == "json" and stdout.strip():
            try:
                parsed = redact(json.loads(stdout))
            except json.JSONDecodeError:
                parsed = None

        return CommandResult(
            args=tuple(command),
            returncode=completed.returncode,
            stdout=stdout,
            stderr=stderr,
            parsed=parsed,
        )

    def version(self) -> CommandResult:
        return self.run(["version", "--output", "json"])

    def auth_status(self) -> CommandResult:
        return self.run(["auth", "status"], output="table")

    def workspace_list(self) -> CommandResult:
        return self.run(["workspace", "list"], output="table")

    def runtime_list(self) -> CommandResult:
        return self.run(["runtime", "list", "--output", "json"])

    def agent_list(self, *, include_archived: bool = False) -> CommandResult:
        args = ["agent", "list", "--output", "json"]
        if include_archived:
            args.append("--include-archived")
        return self.run(args)

    def issue_list(
        self,
        *,
        limit: int = 50,
        status: str | None = None,
        assignee_id: str | None = None,
    ) -> CommandResult:
        args = ["issue", "list", "--output", "json", "--limit", str(limit)]
        if status:
            args.extend(["--status", status])
        if assignee_id:
            args.extend(["--assignee-id", assignee_id])
        return self.run(args)

    def issue_create(
        self,
        title: str,
        *,
        description_file: str | Path | None = None,
        priority: str | None = None,
        status: str | None = None,
        assignee_id: str | None = None,
    ) -> CommandResult:
        args = ["issue", "create", "--output", "json", "--title", title]
        if description_file:
            args.extend(["--description-file", str(description_file)])
        if priority:
            args.extend(["--priority", priority])
        if status:
            args.extend(["--status", status])
        if assignee_id:
            args.extend(["--assignee-id", assignee_id])
        return self.run(args)

    def issue_get(self, issue_id: str) -> CommandResult:
        return self.run(["issue", "get", issue_id, "--output", "json"])

    def issue_runs(self, issue_id: str) -> CommandResult:
        return self.run(["issue", "runs", issue_id, "--output", "json"])

    def issue_comment_list(self, issue_id: str, *, since: str | None = None) -> CommandResult:
        args = ["issue", "comment", "list", issue_id, "--output", "json"]
        if since:
            args.extend(["--since", since])
        return self.run(args)

    def issue_comment_add(
        self,
        issue_id: str,
        *,
        content_file: str | Path,
        parent: str | None = None,
    ) -> CommandResult:
        args = ["issue", "comment", "add", issue_id, "--output", "json", "--content-file", str(content_file)]
        if parent:
            args.extend(["--parent", parent])
        return self.run(args)

    def issue_status(self, issue_id: str, status: str) -> CommandResult:
        return self.run(["issue", "status", issue_id, status, "--output", "json"])

    def issue_run_messages(
        self,
        task_id: str,
        *,
        issue_id: str | None = None,
        since: int | None = None,
    ) -> CommandResult:
        args = ["issue", "run-messages", task_id, "--output", "json"]
        if issue_id:
            args.extend(["--issue", issue_id])
        if since is not None:
            args.extend(["--since", str(since)])
        return self.run(args)
