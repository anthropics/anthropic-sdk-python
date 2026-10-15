from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonError"]


class BetaManagedAgentsOrganizationDisabledDeploymentPausedReasonError(BaseModel):
    """The deployment's organization is disabled."""

    type: Literal["organization_disabled_error"]
