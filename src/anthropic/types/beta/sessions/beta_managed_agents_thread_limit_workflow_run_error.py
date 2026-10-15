from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsThreadLimitWorkflowRunError"]


class BetaManagedAgentsThreadLimitWorkflowRunError(BaseModel):
    """The run exceeded the limit on the number of threads that a run can create."""

    message: str
    """Short explanation written by the server.

    It never contains content from the run or its agents.
    """

    type: Literal["thread_limit_error"]
