from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .beta_web_search_tool_result_error_code import BetaWebSearchToolResultErrorCode

__all__ = ["BetaWebSearchToolRequestErrorObjectParam"]


class BetaWebSearchToolRequestErrorObjectParam(TypedDict, total=False):
    error_code: Required[BetaWebSearchToolResultErrorCode]

    type: Required[Literal["web_search_tool_result_error"]]
