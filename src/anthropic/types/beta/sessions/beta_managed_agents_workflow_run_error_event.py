from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_workflow_run_error import BetaManagedAgentsWorkflowRunError

__all__ = ["BetaManagedAgentsWorkflowRunErrorEvent"]


class BetaManagedAgentsWorkflowRunErrorEvent(BaseModel):
    """A workflow run met an error, or an error kept a run from being created.

    A run that ends with a `result.type` of `error` emits this event before its `workflow_run.status_ended`, with the same `error`.
    """

    id: str
    """Unique identifier for this event."""

    error: BetaManagedAgentsWorkflowRunError
    """Why the run did not finish, or was not created."""

    processed_at: datetime
    """Timestamp when this event was processed."""

    type: Literal["workflow_run.error"]

    workflow_run_id: Optional[str] = None
    """
    Identifier of the run that met the error, or `null` when the error kept a run
    from being created.
    """
