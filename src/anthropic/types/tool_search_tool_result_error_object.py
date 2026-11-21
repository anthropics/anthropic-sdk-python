from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .tool_search_tool_result_error_code import ToolSearchToolResultErrorCode

__all__ = ["ToolSearchToolResultErrorObject"]


class ToolSearchToolResultErrorObject(BaseModel):
    error_code: ToolSearchToolResultErrorCode

    error_message: Optional[str] = None

    type: Literal["tool_search_tool_result_error"]
