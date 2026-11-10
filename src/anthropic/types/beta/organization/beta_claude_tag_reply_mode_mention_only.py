from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagReplyModeMentionOnly"]


class BetaClaudeTagReplyModeMentionOnly(BaseModel):
    """Claude replies only when it is @-mentioned."""

    type: Literal["mention_only"]
