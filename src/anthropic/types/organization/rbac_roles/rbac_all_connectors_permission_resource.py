from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["RBACAllConnectorsPermissionResource"]


class RBACAllConnectorsPermissionResource(BaseModel):
    type: Literal["all_connectors"]
    """Kind of resource the permission applies to."""
