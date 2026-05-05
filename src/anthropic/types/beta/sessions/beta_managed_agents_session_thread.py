# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_session_thread_agent import BetaManagedAgentsSessionThreadAgent
from .beta_managed_agents_session_thread_stats import BetaManagedAgentsSessionThreadStats
from .beta_managed_agents_session_thread_usage import BetaManagedAgentsSessionThreadUsage
from .beta_managed_agents_session_thread_status import BetaManagedAgentsSessionThreadStatus

__all__ = ["BetaManagedAgentsSessionThread"]


class BetaManagedAgentsSessionThread(BaseModel):
    """An execution thread within a `session`.

    Each session has one primary thread plus zero or more child threads spawned by the coordinator.
    """

    id: str
    """Unique identifier for this thread."""

    agent: BetaManagedAgentsSessionThreadAgent
    """Resolved `agent` definition for a single `session_thread`.

    Snapshot of the agent at thread creation time. The multiagent roster is not
    repeated here; read it from `Session.agent`.
    """

    archived_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    created_at: datetime
    """A timestamp in RFC 3339 format"""

    parent_thread_id: Optional[str] = None
    """Parent thread that spawned this thread. Null for the primary thread."""

    session_id: str
    """The session this thread belongs to."""

    stats: Optional[BetaManagedAgentsSessionThreadStats] = None
    """Timing statistics for a session thread."""

    status: BetaManagedAgentsSessionThreadStatus
    """SessionThreadStatus enum"""

    type: Literal["session_thread"]

    updated_at: datetime
    """A timestamp in RFC 3339 format"""

    usage: Optional[BetaManagedAgentsSessionThreadUsage] = None
    """Cumulative token usage for a session thread across all turns."""
