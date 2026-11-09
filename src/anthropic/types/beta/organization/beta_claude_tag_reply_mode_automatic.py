from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagReplyModeAutomatic"]


class BetaClaudeTagReplyModeAutomatic(BaseModel):
    """
    Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.
    """

    type: Literal["automatic"]
