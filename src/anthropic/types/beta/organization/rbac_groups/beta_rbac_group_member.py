from datetime import datetime
from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaRBACGroupMember"]


class BetaRBACGroupMember(BaseModel):
    created_at: datetime
    """RFC 3339 timestamp of when the User was added to the RBAC Group."""

    email: str
    """Email of the User."""

    rbac_group_id: str
    """ID of the RBAC Group."""

    type: Literal["rbac_group_member"]
    """Object type.

    For RBAC Group Members, this is always `"rbac_group_member"`.
    """

    user_id: str
    """ID of the User."""
