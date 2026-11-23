from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_advisor_result_block import BetaAdvisorResultBlock
from .beta_advisor_redacted_result_block import BetaAdvisorRedactedResultBlock
from .beta_advisor_tool_result_error_object import BetaAdvisorToolResultErrorObject

__all__ = ["BetaAdvisorToolResultBlock", "Content"]

Content: TypeAlias = Union[BetaAdvisorToolResultErrorObject, BetaAdvisorResultBlock, BetaAdvisorRedactedResultBlock]


class BetaAdvisorToolResultBlock(BaseModel):
    content: Annotated[Content, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["advisor_tool_result"]
