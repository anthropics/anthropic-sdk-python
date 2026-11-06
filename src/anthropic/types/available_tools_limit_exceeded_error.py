from typing_extensions import Literal

from .._exceptions import BadRequestError
from .available_tools_limit_exceeded_error_details import AvailableToolsLimitExceededErrorDetails

__all__ = ["AvailableToolsLimitExceededError"]


class AvailableToolsLimitExceededError(BadRequestError):
    """
    The tools available after a message exceed a limit on their number or their size.
    """

    error_code: Literal["available_tools_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: AvailableToolsLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
