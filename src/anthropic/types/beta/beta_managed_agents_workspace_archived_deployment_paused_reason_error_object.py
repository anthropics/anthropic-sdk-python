from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsWorkspaceArchivedDeploymentPausedReasonErrorObject(BaseModel):
    """The deployment's workspace was archived."""

    type: Literal["workspace_archived_error"]
