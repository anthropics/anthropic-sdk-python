from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .claude_code_version_too_old_error_details import ClaudeCodeVersionTooOldErrorDetails

__all__ = ["ClaudeCodeVersionTooOldError"]


class ClaudeCodeVersionTooOldError(BadRequestError):
    """
    The request comes from a Claude Code version older than the minimum that the requested model or the organization requires. Update Claude Code, then retry.
    """

    error_code: Literal["claude_code_version_too_old"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ClaudeCodeVersionTooOldErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
