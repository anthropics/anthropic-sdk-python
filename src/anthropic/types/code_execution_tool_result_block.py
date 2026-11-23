from typing_extensions import Literal, Annotated

from .._models import BaseModel, UnionDiscriminator
from .code_execution_tool_result_block_content import CodeExecutionToolResultBlockContent

__all__ = ["CodeExecutionToolResultBlock"]


class CodeExecutionToolResultBlock(BaseModel):
    content: Annotated[CodeExecutionToolResultBlockContent, UnionDiscriminator("type")]

    tool_use_id: str

    type: Literal["code_execution_tool_result"]
