from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaThinkingConfigBetweenToolsParam"]


class BetaThinkingConfigBetweenToolsParam(TypedDict, total=False):
    type: Required[Literal["between_tools"]]
