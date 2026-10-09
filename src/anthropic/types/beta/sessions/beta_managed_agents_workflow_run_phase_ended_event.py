from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunPhaseEndedEvent"]


class BetaManagedAgentsWorkflowRunPhaseEndedEvent(BaseModel):
    """A workflow run's plan left a phase, or the run's end closed it.

    Emitted once for every `workflow_run.phase_started` event, before the run's `workflow_run.status_ended` event. The event does not say whether the plan finished the phase's work, or why it left.
    """

    id: str
    """Unique identifier for this event."""

    phase_started_id: str
    """Identifier of the `workflow_run.phase_started` event that opened the phase."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["workflow_run.phase_ended"]

    workflow_run_id: str
    """Identifier of the run.

    The same value is on all of the run's `workflow_run.*` events.
    """

    workflow_run_phase_id: str
    """
    Identifier of the phase, as in `phases` on the run's `workflow_run.created`
    event.
    """
