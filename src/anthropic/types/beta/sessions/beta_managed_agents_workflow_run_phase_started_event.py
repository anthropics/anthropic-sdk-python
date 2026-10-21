from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunPhaseStartedEvent"]


class BetaManagedAgentsWorkflowRunPhaseStartedEvent(BaseModel):
    """A workflow run's plan entered a phase."""

    id: str
    """Unique identifier for this event."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["workflow_run.phase_started"]

    workflow_run_id: str
    """Identifier of the run.

    The same value is on all of the run's `workflow_run.*` events.
    """

    workflow_run_phase_id: str
    """
    Identifier of the phase, as in `phases` on the run's `workflow_run.created`
    event.
    """
