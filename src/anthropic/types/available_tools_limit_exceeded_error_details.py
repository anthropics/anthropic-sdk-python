from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["AvailableToolsLimitExceededErrorDetails"]


class AvailableToolsLimitExceededErrorDetails(BaseModel):
    """
    The tools available after a message exceed a limit on their number or their size.
    """

    error_code: Literal["available_tools_limit_exceeded"]
