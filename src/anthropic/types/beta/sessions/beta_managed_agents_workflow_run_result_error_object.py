from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_workflow_run_error_object import BetaManagedAgentsWorkflowRunErrorObject

__all__ = ["BetaManagedAgentsWorkflowRunResultErrorObject"]


class BetaManagedAgentsWorkflowRunResultErrorObject(BaseModel):
    """The run failed or reached its time limit."""

    error: BetaManagedAgentsWorkflowRunErrorObject
    """Why the run did not finish."""

    type: Literal["error"]
