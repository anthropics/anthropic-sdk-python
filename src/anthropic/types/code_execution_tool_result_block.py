from typing_extensions import Literal

from .._models import BaseModel
from .code_execution_tool_result_block_content import CodeExecutionToolResultBlockContent

__all__ = ["CodeExecutionToolResultBlock"]


class CodeExecutionToolResultBlock(BaseModel):
    content: CodeExecutionToolResultBlockContent

    tool_use_id: str

    type: Literal["code_execution_tool_result"]
