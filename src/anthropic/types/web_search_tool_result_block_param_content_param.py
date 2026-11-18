from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import TypeAlias

from .web_search_result_block_param import WebSearchResultBlockParam
from .web_search_tool_request_error_object_param import WebSearchToolRequestErrorObjectParam

__all__ = ["WebSearchToolResultBlockParamContentParam"]

WebSearchToolResultBlockParamContentParam: TypeAlias = Union[
    Iterable[WebSearchResultBlockParam], WebSearchToolRequestErrorObjectParam
]
