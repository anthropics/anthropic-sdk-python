from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_claude_code_managed_settings_rbac_groups_mode import BetaClaudeCodeManagedSettingsRBACGroupsMode
from .beta_claude_code_managed_settings_organization_mode import BetaClaudeCodeManagedSettingsOrganizationMode

__all__ = ["BetaClaudeCodeManagedSettingsMode"]

BetaClaudeCodeManagedSettingsMode: TypeAlias = Annotated[
    Union[BetaClaudeCodeManagedSettingsOrganizationMode, BetaClaudeCodeManagedSettingsRBACGroupsMode],
    UnionDiscriminator("type"),
]
