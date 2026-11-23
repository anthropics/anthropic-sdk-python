from typing_extensions import Literal, Annotated

from ..._models import BaseModel, UnionDiscriminator
from .beta_code_execution_tool_result_block_content import BetaCodeExecutionToolResultBlockContent

__all__ = ["BetaCodeExecutionToolResultBlock"]


class BetaCodeExecutionToolResultBlock(BaseModel):
    content: Annotated[BetaCodeExecutionToolResultBlockContent, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["code_execution_tool_result"]
