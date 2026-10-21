from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsManualDeploymentPausedReason"]


class BetaManagedAgentsManualDeploymentPausedReason(BaseModel):
    """The caller invoked the pause endpoint on the deployment."""

    type: Literal["manual"]
