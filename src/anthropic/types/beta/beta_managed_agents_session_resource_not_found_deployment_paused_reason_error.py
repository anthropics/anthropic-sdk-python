# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonError"]


class BetaManagedAgentsSessionResourceNotFoundDeploymentPausedReasonError(BaseModel):
    """A referenced resource no longer exists and its kind was not reported."""

    type: Literal["session_resource_not_found_error"]
