from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsUnknownWorkflowRunError"]


class BetaManagedAgentsUnknownWorkflowRunError(BaseModel):
    """A failure that has no type of its own."""

    message: str
    """Short explanation written by the server.

    It never contains content from the run or its agents.
    """

    type: Literal["unknown_error"]
