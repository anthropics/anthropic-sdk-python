from typing import Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ....._models import BaseModel, UnionDiscriminator
from ..beta_plugin_target_rbac_group import BetaPluginTargetRBACGroup
from ..beta_plugin_target_organization import BetaPluginTargetOrganization
from ..beta_plugin_target_organization_member import BetaPluginTargetOrganizationMember

__all__ = ["BetaPluginInstallationSetting", "Target"]

Target: TypeAlias = Annotated[
    Union[BetaPluginTargetOrganization, BetaPluginTargetRBACGroup, BetaPluginTargetOrganizationMember],
    UnionDiscriminator("type"),
]


class BetaPluginInstallationSetting(BaseModel):
    """The installation setting an organization-owned Plugin holds for one
    target.

    It has no ID of its own: it is addressed by the Plugin's ID and the
    target.
    """

    created_at: datetime
    """When the target was first given a setting for this Plugin."""

    installation_preference: Literal["auto_install", "available", "not_available", "required"]
    """The setting the target holds for this Plugin.

    One of `required`, `auto_install`, `available`, `not_available`; a value this
    API does not yet name is returned as stored.
    """

    plugin_id: str
    """The Plugin's ID."""

    target: Target
    """
    Whose setting this is: `organization` (the Plugin's own organization-wide
    setting) or `rbac_group` (one RBAC Group's own setting); `organization_member`
    does not occur here.
    """

    type: Literal["plugin_installation_setting"]
    """Always `plugin_installation_setting`."""

    updated_at: datetime
    """When its setting last changed."""
