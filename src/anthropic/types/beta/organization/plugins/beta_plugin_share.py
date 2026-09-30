from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ....._models import BaseModel, UnionDiscriminator
from ..beta_plugin_target_rbac_group import BetaPluginTargetRBACGroup
from ..beta_plugin_target_organization import BetaPluginTargetOrganization
from ..beta_plugin_target_organization_member import BetaPluginTargetOrganizationMember

__all__ = ["BetaPluginShare", "Target"]

Target: TypeAlias = Annotated[
    Union[BetaPluginTargetOrganization, BetaPluginTargetRBACGroup, BetaPluginTargetOrganizationMember],
    UnionDiscriminator("type"),
]


class BetaPluginShare(BaseModel):
    """One share the owner of a member-owned Plugin has given.

    Shares are
    read-only in this API and have no ID of their own; who gave a share is
    recorded on the Compliance API activity feed, not here.
    """

    granted_at: datetime
    """
    When the share was given; a share whose role is later changed in claude.ai is
    re-granted and carries the time of that change.
    """

    plugin_id: str
    """The Plugin's ID."""

    target: Target
    """
    Who the Plugin is shared with: `organization` (every member), `rbac_group` (one
    RBAC Group), or `organization_member` (one member).
    """

    type: Literal["plugin_share"]
    """Always `plugin_share`."""
