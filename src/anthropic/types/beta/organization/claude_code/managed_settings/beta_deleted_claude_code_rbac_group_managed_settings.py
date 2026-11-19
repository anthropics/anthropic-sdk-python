from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaDeletedClaudeCodeRBACGroupManagedSettings"]


class BetaDeletedClaudeCodeRBACGroupManagedSettings(BaseModel):
    rbac_group_id: str
    """The RBAC Group's ID, prefixed `rbac_group_`."""

    type: Literal["claude_code_rbac_group_managed_settings_deleted"]
    """Always `claude_code_rbac_group_managed_settings_deleted`."""
