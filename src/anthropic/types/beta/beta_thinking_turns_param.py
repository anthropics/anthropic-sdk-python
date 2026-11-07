from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaThinkingTurnsParam"]


class BetaThinkingTurnsParam(TypedDict, total=False):
    type: Required[Literal["thinking_turns"]]

    value: Required[int]
