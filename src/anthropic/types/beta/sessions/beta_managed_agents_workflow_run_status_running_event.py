from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunStatusRunningEvent"]


class BetaManagedAgentsWorkflowRunStatusRunningEvent(BaseModel):
    """A workflow run is running.

    Emitted when the run starts to execute, and each time it resumes after being idle. A run that starts idle emits `workflow_run.status_idle` first.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["workflow_run.status_running"]

    workflow_run_id: str
    """Identifier of the run.

    The same value is on all of the run's `workflow_run.*` events.
    """
