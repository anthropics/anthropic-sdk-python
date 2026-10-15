from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunResultCompleted"]


class BetaManagedAgentsWorkflowRunResultCompleted(BaseModel):
    """The run's plan, a program that the agent wrote, finished.

    This does not say whether the work succeeded.
    """

    type: Literal["completed"]
