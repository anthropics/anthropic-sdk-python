from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagReplyModeMentionOnlyParam"]


class BetaClaudeTagReplyModeMentionOnlyParam(TypedDict, total=False):
    """Claude replies only when it is @-mentioned."""

    type: Required[Literal["mention_only"]]
