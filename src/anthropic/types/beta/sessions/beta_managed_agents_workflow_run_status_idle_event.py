from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunStatusIdleEvent"]


class BetaManagedAgentsWorkflowRunStatusIdleEvent(BaseModel):
    """A workflow run is idle.

    Emitted each time the run goes idle, whatever the cause. If the run ends while idle, no `workflow_run.status_running` comes between this event and its `workflow_run.status_ended`.
    """

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["workflow_run.status_idle"]

    workflow_run_id: str
    """Identifier of the run.

    The same value is on all of the run's `workflow_run.*` events.
    """
