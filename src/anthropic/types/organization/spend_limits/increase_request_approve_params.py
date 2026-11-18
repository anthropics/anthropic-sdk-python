from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..spend_limit_period import SpendLimitPeriod

__all__ = ["IncreaseRequestApproveParams"]


class IncreaseRequestApproveParams(TypedDict, total=False):
    amount: Required[str]
    """
    New per-user spend limit as a non-negative integer decimal string (minor units).
    """

    period: Optional[SpendLimitPeriod]

    suppress_notification: bool
