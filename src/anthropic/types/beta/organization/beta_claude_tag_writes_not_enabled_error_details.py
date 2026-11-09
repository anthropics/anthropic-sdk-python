from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagWritesNotEnabledErrorDetails"]


class BetaClaudeTagWritesNotEnabledErrorDetails(BaseModel):
    """Changes through the Claude Tag API are not enabled for the organization."""

    error_code: Literal["claude_tag_writes_not_enabled"]
