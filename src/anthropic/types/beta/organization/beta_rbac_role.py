from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaRBACRole"]


class BetaRBACRole(BaseModel):
    id: str
    """ID of the RBAC Role."""

    created_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was created."""

    name: str
    """Name of the RBAC Role."""

    type: Literal["rbac_role"]
    """Object type.

    For RBAC Roles, this is always `"rbac_role"`.
    """

    updated_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was last updated."""
