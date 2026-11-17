from typing import List, Union
from typing_extensions import TypeAlias

from .beta_web_search_result_block import BetaWebSearchResultBlock
from .beta_web_search_tool_result_error_object import BetaWebSearchToolResultErrorObject

__all__ = ["BetaWebSearchToolResultBlockContent"]

BetaWebSearchToolResultBlockContent: TypeAlias = Union[
    BetaWebSearchToolResultErrorObject, List[BetaWebSearchResultBlock]
]
