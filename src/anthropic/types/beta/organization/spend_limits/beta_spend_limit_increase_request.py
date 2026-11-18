from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel
from ..beta_spend_summary import BetaSpendSummary
from ..beta_spend_limit_period import BetaSpendLimitPeriod
from .beta_spend_limit_increase_request_actor import BetaSpendLimitIncreaseRequestActor
from .beta_spend_limit_increase_request_status import BetaSpendLimitIncreaseRequestStatus
from .beta_spend_limit_increase_request_resolved_by import BetaSpendLimitIncreaseRequestResolvedBy

__all__ = ["BetaSpendLimitIncreaseRequest"]


class BetaSpendLimitIncreaseRequest(BaseModel):
    id: str

    actor: BetaSpendLimitIncreaseRequestActor
    """Who submitted the increase request."""

    created_at: datetime

    period: BetaSpendLimitPeriod

    resolved_at: Optional[datetime] = None

    resolved_by: Optional[BetaSpendLimitIncreaseRequestResolvedBy] = None
    """Who approved or denied the increase request."""

    spend_summary: Optional[BetaSpendSummary] = None
    """Per-member effective-limit report row (`GET /spend_limits/effective`)."""

    status: BetaSpendLimitIncreaseRequestStatus

    type: Literal["spend_limit_increase_request"]
