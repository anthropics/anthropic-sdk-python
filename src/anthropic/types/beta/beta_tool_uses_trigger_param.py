from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaToolUsesTriggerParam"]


class BetaToolUsesTriggerParam(TypedDict, total=False):
    type: Required[Literal["tool_uses"]]

    value: Required[int]
