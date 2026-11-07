from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_workflow_run_phase import BetaManagedAgentsWorkflowRunPhase

__all__ = ["BetaManagedAgentsWorkflowRunCreatedEvent"]


class BetaManagedAgentsWorkflowRunCreatedEvent(BaseModel):
    """A workflow run was created.

    A workflow run is background work that the session's agent starts. Emitted once per run, before the run's other `workflow_run.*` events.
    """

    id: str
    """Unique identifier for this event."""

    description: Optional[str] = None
    """
    Description that the agent gave the run, passed on as written, or `null` if it
    gave none.
    """

    name: str
    """
    Name that the agent gave the run, passed on as written, or a name that the
    server assigned.
    """

    phases: List[BetaManagedAgentsWorkflowRunPhase]
    """The phases that the run's plan declares, in the plan's order. Can be empty."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["workflow_run.created"]

    workflow_run_id: str
    """Identifier of the run.

    The same value is on all of the run's `workflow_run.*` events.
    """
