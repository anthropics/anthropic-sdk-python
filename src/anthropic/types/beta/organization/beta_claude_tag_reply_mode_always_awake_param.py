from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagReplyModeAlwaysAwakeParam"]


class BetaClaudeTagReplyModeAlwaysAwakeParam(TypedDict, total=False):
    """Like `automatic`, but Claude never pauses on its own.

    Available where it is enabled for the channel.
    """

    type: Required[Literal["always_awake"]]
