"""Lightweight data models for the Multica CLI adapter."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal


OutputKind = Literal["json", "table", "text"]


@dataclass(frozen=True)
class CommandResult:
    """Normalized result from a Multica CLI invocation."""

    args: tuple[str, ...]
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool = False
    parsed: Any | None = None

    @property
    def ok(self) -> bool:
        return self.returncode == 0 and not self.timed_out


@dataclass(frozen=True)
class CapabilityCheck:
    """Recorded outcome for one CLI capability probe."""

    name: str
    command: tuple[str, ...]
    ok: bool
    returncode: int
    output_kind: OutputKind
    timed_out: bool = False
    summary: str | None = None
    data: Any | None = None
    error: str | None = None
