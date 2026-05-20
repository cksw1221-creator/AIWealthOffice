"""GenericAgent bridge helpers for the Multica CLI."""

from .closure_sync import apply_local_closure_sync
from .ceo import (
    DEFAULT_CLOSURE_MANIFEST_PATH,
    DEFAULT_CONTINUITY_PATH,
    DEFAULT_REGISTRY_PATH,
    SESSION_MODES,
    dispatch_issue,
    load_session_continuity,
    load_worker_registry,
    resolve_worker,
    review_issue,
)
from .client import MulticaClient, redact
from .models import CapabilityCheck, CommandResult
from .polling import format_issue_summary, poll_issue

__all__ = [
    "CapabilityCheck",
    "CommandResult",
    "DEFAULT_CLOSURE_MANIFEST_PATH",
    "DEFAULT_CONTINUITY_PATH",
    "DEFAULT_REGISTRY_PATH",
    "MulticaClient",
    "SESSION_MODES",
    "apply_local_closure_sync",
    "dispatch_issue",
    "format_issue_summary",
    "load_session_continuity",
    "load_worker_registry",
    "poll_issue",
    "redact",
    "resolve_worker",
    "review_issue",
]
