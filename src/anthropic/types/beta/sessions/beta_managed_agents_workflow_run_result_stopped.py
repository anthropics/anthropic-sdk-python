from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunResultStopped"]


class BetaManagedAgentsWorkflowRunResultStopped(BaseModel):
    """The agent stopped the run."""

    type: Literal["stopped"]
