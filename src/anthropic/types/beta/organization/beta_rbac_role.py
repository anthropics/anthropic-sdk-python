from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_rbac_role_source import BetaRBACRoleSource

__all__ = ["BetaRBACRole"]


class BetaRBACRole(BaseModel):
    id: str
    """ID of the RBAC Role."""

    created_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was created."""

    display_name: str
    """Name of the RBAC Role.

    For a built-in role, this is Anthropic's name for the access that the role
    grants. Anthropic may change this name, so to keep a lasting reference to a
    role, store its `id`.
    """

    source: BetaRBACRoleSource
    """Whether the RBAC Role is built-in or custom.

    More values of `type` may be added, so do not treat every role that is not
    `built_in` as `custom`.
    """

    type: Literal["rbac_role"]
    """Object type.

    For RBAC Roles, this is always `"rbac_role"`.
    """

    updated_at: datetime
    """RFC 3339 datetime string indicating when the RBAC Role was last updated."""
