from typing import List, Union
from typing_extensions import TypeAlias

from .web_search_result_block import WebSearchResultBlock
from .web_search_tool_result_error import WebSearchToolResultError

__all__ = ["WebSearchToolResultBlockContent"]

WebSearchToolResultBlockContent: TypeAlias = Union[WebSearchToolResultError, List[WebSearchResultBlock]]
