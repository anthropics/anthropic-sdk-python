from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagReplyModeAutomaticParam"]


class BetaClaudeTagReplyModeAutomaticParam(TypedDict, total=False):
    """
    Claude reads along and joins in when it can help, and pauses on its own in quiet or busy channels.
    """

    type: Required[Literal["automatic"]]
