from typing_extensions import Literal

from ..._exceptions import RateLimitError
from .ramp_limit_exceeded_error_details import RampLimitExceededErrorDetails

__all__ = ["RampLimitExceededError"]


class RampLimitExceededError(RateLimitError):
    """The request would exceed a ramp limit, which caps how fast usage can grow.

    Retry after the time in the `retry-after` header.
    """

    error_code: Literal["ramp_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: RampLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
