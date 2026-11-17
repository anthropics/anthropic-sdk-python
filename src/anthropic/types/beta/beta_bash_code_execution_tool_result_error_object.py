from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaBashCodeExecutionToolResultErrorObject"]


class BetaBashCodeExecutionToolResultErrorObject(BaseModel):
    error_code: Literal[
        "invalid_tool_input", "unavailable", "too_many_requests", "execution_time_exceeded", "output_file_too_large"
    ]

    type: Literal["bash_code_execution_tool_result_error"]
