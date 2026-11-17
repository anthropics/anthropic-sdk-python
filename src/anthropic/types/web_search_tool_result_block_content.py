from typing import List, Union
from typing_extensions import TypeAlias

from .web_search_result_block import WebSearchResultBlock
from .web_search_tool_result_error_object import WebSearchToolResultErrorObject

__all__ = ["WebSearchToolResultBlockContent"]

WebSearchToolResultBlockContent: TypeAlias = Union[WebSearchToolResultErrorObject, List[WebSearchResultBlock]]
