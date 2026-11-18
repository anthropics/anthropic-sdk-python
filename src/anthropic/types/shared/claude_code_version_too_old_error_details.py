from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ClaudeCodeVersionTooOldErrorDetails"]


class ClaudeCodeVersionTooOldErrorDetails(BaseModel):
    """
    The request comes from a Claude Code version older than the minimum that the requested model or the organization requires. Update Claude Code, then retry.
    """

    error_code: Literal["claude_code_version_too_old"]
