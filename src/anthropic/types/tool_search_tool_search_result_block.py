from typing import List
from typing_extensions import Literal

from .._models import BaseModel
from .tool_reference_block import ToolReferenceBlock

__all__ = ["ToolSearchToolSearchResultBlock"]


class ToolSearchToolSearchResultBlock(BaseModel):
    tool_references: List[ToolReferenceBlock]

    type: Literal["tool_search_tool_search_result"]
