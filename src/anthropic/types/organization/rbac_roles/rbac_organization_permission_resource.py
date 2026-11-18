from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["RBACOrganizationPermissionResource"]


class RBACOrganizationPermissionResource(BaseModel):
    organization_id: str
    """UUID of the organization the permission applies to."""

    type: Literal["organization"]
    """Kind of resource the permission applies to."""
