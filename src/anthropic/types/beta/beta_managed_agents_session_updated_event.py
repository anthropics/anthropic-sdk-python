from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_budget_limit import BetaManagedAgentsBudgetLimit
from .beta_managed_agents_session_agent import BetaManagedAgentsSessionAgent

__all__ = ["BetaManagedAgentsSessionUpdatedEvent"]


class BetaManagedAgentsSessionUpdatedEvent(BaseModel):
    """Emitted when an UpdateSession request changed at least one field.

    Carries only the fields that changed; absent fields were not part of the update. The new configuration applies from the next turn.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when the update was applied."""

    type: Literal["session.updated"]

    agent: Optional[BetaManagedAgentsSessionAgent] = None
    """The session's effective agent configuration after the update.

    Present only when the update changed `agent` (tools or mcp_servers); when
    present it is the full materialised snapshot, not a diff.
    """

    budget: Optional[BetaManagedAgentsBudgetLimit] = None
    """
    The session's budget after the update: the new budget when set or replaced, or
    null when the update removed it. Present only when the update changed the
    budget.
    """

    metadata: Optional[Dict[str, str]] = None
    """The session's full metadata bag after the update.

    Present when the update set non-empty metadata; absent when metadata was
    unchanged or cleared to empty.
    """

    title: Optional[str] = None
    """The session's new title. Present only when the update changed it."""
