from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_tool_search_tool_result_error_object import BetaToolSearchToolResultErrorObject
from .beta_tool_search_tool_search_result_block import BetaToolSearchToolSearchResultBlock

__all__ = ["BetaToolSearchToolResultBlock", "Content"]

Content: TypeAlias = Union[BetaToolSearchToolResultErrorObject, BetaToolSearchToolSearchResultBlock]


class BetaToolSearchToolResultBlock(BaseModel):
    content: Annotated[Content, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["tool_search_tool_result"]
