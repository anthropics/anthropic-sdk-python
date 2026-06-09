# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSessionRateLimitedRunError"]


class BetaManagedAgentsSessionRateLimitedRunError(BaseModel):
    """Session creation was rejected due to rate limiting.

    The schedule keeps firing; subsequent runs may succeed.
    """

    message: str
    """Human-readable error description."""

    type: Literal["session_rate_limited_error"]
