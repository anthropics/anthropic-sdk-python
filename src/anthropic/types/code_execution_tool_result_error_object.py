from typing_extensions import Literal

from .._models import BaseModel
from .code_execution_tool_result_error_code import CodeExecutionToolResultErrorCode

__all__ = ["CodeExecutionToolResultErrorObject"]


class CodeExecutionToolResultErrorObject(BaseModel):
    error_code: CodeExecutionToolResultErrorCode

    type: Literal["code_execution_tool_result_error"]
