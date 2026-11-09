from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from ..spend_limit import SpendLimit
from ..spend_summary import SpendSummary
from ..spend_limit_period import SpendLimitPeriod
from .spend_limit_increase_request_actor import SpendLimitIncreaseRequestActor
from .spend_limit_increase_request_status import SpendLimitIncreaseRequestStatus
from .spend_limit_increase_request_resolved_by import SpendLimitIncreaseRequestResolvedBy

__all__ = ["IncreaseRequestApproveResponse"]


class IncreaseRequestApproveResponse(BaseModel):
    id: str

    actor: SpendLimitIncreaseRequestActor
    """Who submitted the increase request."""

    created_at: datetime

    period: SpendLimitPeriod

    resolved_at: Optional[datetime] = None

    resolved_by: Optional[SpendLimitIncreaseRequestResolvedBy] = None
    """Who approved or denied the increase request."""

    spend_limit: Optional[SpendLimit] = None
    """A configured spend limit: a cap on metered spend for one scope and period."""

    spend_summary: Optional[SpendSummary] = None
    """Per-member effective-limit report row (`GET /spend_limits/effective`)."""

    status: SpendLimitIncreaseRequestStatus

    type: Literal["spend_limit_increase_request"]
