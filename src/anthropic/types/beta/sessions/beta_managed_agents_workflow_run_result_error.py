from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_workflow_run_error import BetaManagedAgentsWorkflowRunError

__all__ = ["BetaManagedAgentsWorkflowRunResultError"]


class BetaManagedAgentsWorkflowRunResultError(BaseModel):
    """The run failed or reached its time limit."""

    error: BetaManagedAgentsWorkflowRunError
    """Why the run did not finish."""

    type: Literal["error"]
