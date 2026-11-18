from typing_extensions import Literal

from ..._exceptions import RateLimitError
from .enforced_spend_limit_reached_error_details import EnforcedSpendLimitReachedErrorDetails

__all__ = ["EnforcedSpendLimitReachedError"]


class EnforcedSpendLimitReachedError(RateLimitError):
    """The organization has crossed the monthly API usage threshold of its API tier."""

    error_code: Literal["enforced_spend_limit_reached"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: EnforcedSpendLimitReachedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
