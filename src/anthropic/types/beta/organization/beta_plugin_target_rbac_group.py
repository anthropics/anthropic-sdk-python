from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginTargetRBACGroup"]


class BetaPluginTargetRBACGroup(BaseModel):
    rbac_group_id: str
    """The RBAC Group's ID."""

    type: Literal["rbac_group"]
    """An RBAC Group."""
