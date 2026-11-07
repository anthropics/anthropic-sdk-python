from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsMaxWorkflowRunsWorkflowRunError"]


class BetaManagedAgentsMaxWorkflowRunsWorkflowRunError(BaseModel):
    """
    No run was created, because the session was at its limit of open workflow runs, which are runs that have not ended. Only `workflow_run.error` carries this type.
    """

    message: str
    """Short explanation written by the server.

    It never contains content from the run or its agents.
    """

    type: Literal["max_workflow_runs_error"]
