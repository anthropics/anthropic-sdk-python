from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsTimeoutWorkflowRunError"]


class BetaManagedAgentsTimeoutWorkflowRunError(BaseModel):
    """The run reached its time limit."""

    message: str
    """Short explanation written by the server.

    It never contains content from the run or its agents.
    """

    type: Literal["timeout_error"]
