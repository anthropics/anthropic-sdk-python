from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["RBACRole"]


class RBACRole(BaseModel):
    id: str
    """ID of the RBAC Role."""

    created_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was created."""

    display_name: str
    """Name of the RBAC Role.

    For a role created by Anthropic, this is Anthropic's name for the access that
    the role grants. Anthropic may change this name, so to keep a lasting reference
    to a role, store its `id`.
    """

    type: Literal["rbac_role"]
    """Object type.

    For RBAC Roles, this is always `"rbac_role"`.
    """

    updated_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was last updated."""
