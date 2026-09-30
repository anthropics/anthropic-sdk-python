from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["MemberRemoveResponse"]


class MemberRemoveResponse(BaseModel):
    rbac_group_id: str
    """ID of the RBAC Group."""

    type: Literal["rbac_group_member_deleted"]
    """Deleted object type.

    For RBAC Group Members, this is always `"rbac_group_member_deleted"`.
    """

    user_id: str
    """ID of the User."""
