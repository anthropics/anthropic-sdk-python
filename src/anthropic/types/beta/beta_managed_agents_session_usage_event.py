# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

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
    """A timestamp in RFC 3339 format"""

    type: Literal["session.usage"]

    usage: BetaManagedAgentsSessionUsageSnapshot
    """Point-in-time snapshot of a session's cumulative usage."""

    budget: Optional[BetaManagedAgentsBudgetLimit] = None
    """A hard spend ceiling.

    The session stops issuing new model requests once the tracked list cost reaches
    `max_list_cost`.
    """
