"""GenericAgent bridge helpers for the Multica CLI."""

from .client import MulticaClient, redact
from .models import CapabilityCheck, CommandResult

__all__ = ["CapabilityCheck", "CommandResult", "MulticaClient", "redact"]
