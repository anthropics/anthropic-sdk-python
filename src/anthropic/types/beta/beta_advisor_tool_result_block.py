from typing import Union
from typing_extensions import Literal, TypeAlias

from ..._models import BaseModel
from .beta_advisor_result_block import BetaAdvisorResultBlock
from .beta_advisor_redacted_result_block import BetaAdvisorRedactedResultBlock
from .beta_advisor_tool_result_error_object import BetaAdvisorToolResultErrorObject

__all__ = ["BetaAdvisorToolResultBlock", "Content"]

Content: TypeAlias = Union[BetaAdvisorToolResultErrorObject, BetaAdvisorResultBlock, BetaAdvisorRedactedResultBlock]


class BetaAdvisorToolResultBlock(BaseModel):
    content: Content

    tool_use_id: str

    type: Literal["advisor_tool_result"]
