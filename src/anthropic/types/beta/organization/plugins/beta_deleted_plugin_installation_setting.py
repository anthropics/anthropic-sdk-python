from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ....._models import BaseModel, UnionDiscriminator
from ..beta_plugin_target_rbac_group import BetaPluginTargetRBACGroup
from ..beta_plugin_target_organization import BetaPluginTargetOrganization
from ..beta_plugin_target_organization_member import BetaPluginTargetOrganizationMember

__all__ = ["BetaDeletedPluginInstallationSetting", "Target"]

Target: TypeAlias = Annotated[
    Union[BetaPluginTargetOrganization, BetaPluginTargetRBACGroup, BetaPluginTargetOrganizationMember],
    UnionDiscriminator("type"),
]


class BetaDeletedPluginInstallationSetting(BaseModel):
    """
    Confirmation that one target's installation setting was removed, naming
    the Plugin and the target in place of an ID.
    """

    plugin_id: str
    """The Plugin's ID."""

    target: Target
    """Whose setting was removed."""

    type: Literal["plugin_installation_setting_deleted"]
    """Always `plugin_installation_setting_deleted`."""
