from typing_extensions import Literal

from ..._models import BaseModel
from .beta_web_search_tool_result_error_code import BetaWebSearchToolResultErrorCode

__all__ = ["BetaWebSearchToolResultError"]


class BetaWebSearchToolResultError(BaseModel):
    error_code: BetaWebSearchToolResultErrorCode

    type: Literal["web_search_tool_result_error"]
