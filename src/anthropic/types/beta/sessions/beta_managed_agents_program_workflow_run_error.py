from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsProgramWorkflowRunError"]


class BetaManagedAgentsProgramWorkflowRunError(BaseModel):
    """The plan, a program that the agent wrote, failed, or the server refused it."""

    message: str
    """Short explanation written by the server.

    It never contains content from the run or its agents.
    """

    type: Literal["program_error"]
