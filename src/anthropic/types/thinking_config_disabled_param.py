from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ThinkingConfigDisabledParam"]


class ThinkingConfigDisabledParam(TypedDict, total=False):
    type: Required[Literal["disabled"]]
