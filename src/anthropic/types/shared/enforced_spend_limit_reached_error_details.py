from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["EnforcedSpendLimitReachedErrorDetails"]


class EnforcedSpendLimitReachedErrorDetails(BaseModel):
    """The organization has crossed the monthly API usage threshold of its API tier."""

    error_code: Literal["enforced_spend_limit_reached"]
