from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonError"]


class BetaManagedAgentsEnvironmentArchivedDeploymentPausedReasonError(BaseModel):
    """The deployment's environment was archived."""

    type: Literal["environment_archived_error"]
