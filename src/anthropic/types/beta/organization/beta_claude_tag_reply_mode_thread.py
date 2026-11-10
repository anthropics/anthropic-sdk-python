from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagReplyModeThread"]


class BetaClaudeTagReplyModeThread(BaseModel):
    """
    Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.
    """

    type: Literal["thread"]
