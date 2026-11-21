from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsOrganizationDisabledRunErrorObject"]


class BetaManagedAgentsOrganizationDisabledRunErrorObject(BaseModel):
    """The deployment's organization is disabled."""

    message: str
    """Human-readable error description."""

    type: Literal["organization_disabled_error"]
