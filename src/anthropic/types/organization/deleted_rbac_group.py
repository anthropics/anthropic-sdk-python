from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["DeletedRBACGroup"]


class DeletedRBACGroup(BaseModel):
    id: str
    """ID of the RBAC Group."""

    type: Literal["rbac_group_deleted"]
    """Deleted object type.

    For RBAC Groups, this is always `"rbac_group_deleted"`.
    """
