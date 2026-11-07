from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_workflow_run_result import BetaManagedAgentsWorkflowRunResult

__all__ = ["BetaManagedAgentsWorkflowRunStatusEndedEvent"]


class BetaManagedAgentsWorkflowRunStatusEndedEvent(BaseModel):
    """A workflow run ended.

    Emitted once per run, as the last of the run's `workflow_run.*` events.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    result: BetaManagedAgentsWorkflowRunResult
    """How the run ended."""

    type: Literal["workflow_run.status_ended"]

    workflow_run_id: str
    """Identifier of the run.

    The same value is on all of the run's `workflow_run.*` events.
    """
