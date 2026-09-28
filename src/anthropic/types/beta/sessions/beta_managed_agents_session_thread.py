from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from ..beta_managed_agents_advisor import BetaManagedAgentsAdvisor
from .beta_managed_agents_session_thread_stats import BetaManagedAgentsSessionThreadStats
from .beta_managed_agents_session_thread_usage import BetaManagedAgentsSessionThreadUsage
from ..beta_managed_agents_session_thread_agent import BetaManagedAgentsSessionThreadAgent
from .beta_managed_agents_session_thread_status import BetaManagedAgentsSessionThreadStatus

__all__ = ["BetaManagedAgentsSessionThread", "Agent"]

Agent: TypeAlias = Annotated[
    Union[BetaManagedAgentsSessionThreadAgent, BetaManagedAgentsAdvisor], UnionDiscriminator("type")
]


class BetaManagedAgentsSessionThread(BaseModel):
    """An execution thread within a `session`.

    Each session has one primary thread plus zero or more child threads spawned by the coordinator.
    """

    id: str
    """Unique identifier for this thread."""

    agent: Agent
    """Resolved agent definition for this thread.

    Snapshot of the agent at thread creation time.
    """

    archived_at: Optional[datetime] = None
    """When the thread was archived. Null if not archived."""

    created_at: datetime
    """When the thread was created."""

    parent_thread_id: Optional[str] = None
    """Parent thread that spawned this thread. Null for the primary thread."""

    session_id: str
    """The session this thread belongs to."""

    stats: Optional[BetaManagedAgentsSessionThreadStats] = None
    """Timing statistics for this thread.

    Null until the thread's first status transition.
    """

    status: BetaManagedAgentsSessionThreadStatus
    """Current execution status of the thread."""

    type: Literal["session_thread"]

    updated_at: datetime
    """When the thread was last updated."""

    usage: Optional[BetaManagedAgentsSessionThreadUsage] = None
    """Cumulative token usage for this thread.

    Null until the thread's first idle transition.
    """
