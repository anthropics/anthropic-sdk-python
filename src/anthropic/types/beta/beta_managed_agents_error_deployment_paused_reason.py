# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_deployment_paused_reason_error import BetaManagedAgentsDeploymentPausedReasonError

__all__ = ["BetaManagedAgentsErrorDeploymentPausedReason"]


class BetaManagedAgentsErrorDeploymentPausedReason(BaseModel):
    """A scheduled fire recorded a failed run whose error auto-pauses the deployment."""

    error: BetaManagedAgentsDeploymentPausedReasonError
    """The error that triggered an auto-pause. Matches the failed run's `error.type`."""

    type: Literal["error"]
