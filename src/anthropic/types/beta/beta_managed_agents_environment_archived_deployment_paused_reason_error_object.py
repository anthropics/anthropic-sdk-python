from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonErrorObject(BaseModel):
    """The deployment's environment was archived."""

    type: Literal["environment_archived_error"]
