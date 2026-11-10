from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagReplyModeThreadParam"]


class BetaClaudeTagReplyModeThreadParam(TypedDict, total=False):
    """
    Every new top-level message in the channel gets its own reply from Claude, in a thread under it. Available where it is enabled for the channel, and only once Claude has been used in the channel.
    """

    type: Required[Literal["thread"]]
