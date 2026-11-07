from typing_extensions import Literal, TypeAlias

__all__ = ["ToolSearchToolResultErrorCode"]

ToolSearchToolResultErrorCode: TypeAlias = Literal[
    "invalid_tool_input", "unavailable", "too_many_requests", "execution_time_exceeded"
]
