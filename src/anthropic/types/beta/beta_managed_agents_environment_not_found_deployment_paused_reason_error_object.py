from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsEnvironmentNotFoundDeploymentPausedReasonErrorObject(BaseModel):
    """The deployment's environment no longer exists."""

    type: Literal["environment_not_found_error"]
