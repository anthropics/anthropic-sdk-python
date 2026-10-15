from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ThinkingConfigBetweenToolsParam"]


class ThinkingConfigBetweenToolsParam(TypedDict, total=False):
    type: Required[Literal["between_tools"]]
