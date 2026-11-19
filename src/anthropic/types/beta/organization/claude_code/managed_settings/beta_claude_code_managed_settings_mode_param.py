from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_claude_code_managed_settings_rbac_groups_mode_param import BetaClaudeCodeManagedSettingsRBACGroupsModeParam
from .beta_claude_code_managed_settings_organization_mode_param import (
    BetaClaudeCodeManagedSettingsOrganizationModeParam,
)

__all__ = ["BetaClaudeCodeManagedSettingsModeParam"]

BetaClaudeCodeManagedSettingsModeParam: TypeAlias = Union[
    BetaClaudeCodeManagedSettingsOrganizationModeParam, BetaClaudeCodeManagedSettingsRBACGroupsModeParam
]
