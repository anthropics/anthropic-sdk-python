from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_claude_tag_writes_not_enabled_error_details import BetaClaudeTagWritesNotEnabledErrorDetails

__all__ = ["BetaClaudeTagWritesNotEnabledError"]


class BetaClaudeTagWritesNotEnabledError(PermissionDeniedError):
    """Changes through the Claude Tag API are not enabled for the organization."""

    error_code: Literal["claude_tag_writes_not_enabled"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaClaudeTagWritesNotEnabledErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
