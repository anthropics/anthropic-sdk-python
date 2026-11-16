from typing_extensions import Literal

from .._models import BaseModel
from .bash_code_execution_tool_result_error_code import BashCodeExecutionToolResultErrorCode

__all__ = ["BashCodeExecutionToolResultErrorObject"]


class BashCodeExecutionToolResultErrorObject(BaseModel):
    error_code: BashCodeExecutionToolResultErrorCode

    type: Literal["bash_code_execution_tool_result_error"]
