from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagReplyModeAlwaysAwake"]


class BetaClaudeTagReplyModeAlwaysAwake(BaseModel):
    """Like `automatic`, but Claude never pauses on its own.

    Available where it is enabled for the channel.
    """

    type: Literal["always_awake"]
