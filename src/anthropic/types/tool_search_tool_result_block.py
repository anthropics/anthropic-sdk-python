from typing import Union
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .tool_search_tool_result_error_object import ToolSearchToolResultErrorObject
from .tool_search_tool_search_result_block import ToolSearchToolSearchResultBlock

__all__ = ["ToolSearchToolResultBlock", "Content"]

Content: TypeAlias = Union[ToolSearchToolResultErrorObject, ToolSearchToolSearchResultBlock]


class ToolSearchToolResultBlock(BaseModel):
    content: Content

    tool_use_id: str

    type: Literal["tool_search_tool_result"]
