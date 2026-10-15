from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_budget_limit import BetaManagedAgentsBudgetLimit
from .sessions.beta_managed_agents_session_usage_snapshot import BetaManagedAgentsSessionUsageSnapshot

__all__ = ["BetaManagedAgentsSessionUsageEvent"]


class BetaManagedAgentsSessionUsageEvent(BaseModel):
    """Periodic snapshot of the session's cumulative usage and tracked list cost."""

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when the snapshot was taken."""

    type: Literal["session.usage"]

    usage: BetaManagedAgentsSessionUsageSnapshot
    """The session's cumulative usage at the snapshot time."""

    budget: Optional[BetaManagedAgentsBudgetLimit] = None
    """
    The session's configured budget at the snapshot time, or null when the session
    has no budget.
    """
