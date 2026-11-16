from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import TypeAlias

from .beta_web_search_result_block_param import BetaWebSearchResultBlockParam
from .beta_web_search_tool_request_error_object_param import BetaWebSearchToolRequestErrorObjectParam

__all__ = ["BetaWebSearchToolResultBlockParamContentParam"]

BetaWebSearchToolResultBlockParamContentParam: TypeAlias = Union[
    Iterable[BetaWebSearchResultBlockParam], BetaWebSearchToolRequestErrorObjectParam
]
