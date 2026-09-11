from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaAllThinkingTurnsParam"]


class BetaAllThinkingTurnsParam(TypedDict, total=False):
    type: Required[Literal["all"]]
