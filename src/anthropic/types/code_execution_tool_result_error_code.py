from typing_extensions import Literal, TypeAlias

__all__ = ["CodeExecutionToolResultErrorCode"]

CodeExecutionToolResultErrorCode: TypeAlias = Literal[
    "invalid_tool_input", "unavailable", "too_many_requests", "execution_time_exceeded"
]
