from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_tool_reference_block import BetaToolReferenceBlock

__all__ = ["BetaToolSearchToolSearchResultBlock"]


class BetaToolSearchToolSearchResultBlock(BaseModel):
    tool_references: List[BetaToolReferenceBlock]

    type: Literal["tool_search_tool_search_result"]
