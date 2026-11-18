from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RampLimitExceededErrorDetails"]


class RampLimitExceededErrorDetails(BaseModel):
    """The request would exceed a ramp limit, which caps how fast usage can grow.

    Retry after the time in the `retry-after` header.
    """

    error_code: Literal["ramp_limit_exceeded"]
