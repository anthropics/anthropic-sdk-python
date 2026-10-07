from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaRBACRole"]


class BetaRBACRole(BaseModel):
    id: str
    """ID of the RBAC Role."""

    created_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was created."""

    display_name: str
    """Name of the RBAC Role.

    For a role created by Anthropic, this name can differ from the label claude.ai
    shows, and Anthropic may change the name. To keep a lasting reference to a role,
    store its `id`.
    """

    name: str
    """Deprecated: use `display_name` instead.

    Name of the RBAC Role; always the same value as `display_name`.
    """

    type: Literal["rbac_role"]
    """Object type.

    For RBAC Roles, this is always `"rbac_role"`.
    """

    updated_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was last updated."""
