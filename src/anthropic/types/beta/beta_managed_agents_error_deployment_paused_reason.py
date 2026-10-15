from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_deployment_paused_reason_error import BetaManagedAgentsDeploymentPausedReasonError

__all__ = ["BetaManagedAgentsErrorDeploymentPausedReason"]


class BetaManagedAgentsErrorDeploymentPausedReason(BaseModel):
    """A scheduled fire recorded a failed run whose error auto-pauses the deployment."""

    error: BetaManagedAgentsDeploymentPausedReasonError
    """The failed run's error."""

    type: Literal["error"]
