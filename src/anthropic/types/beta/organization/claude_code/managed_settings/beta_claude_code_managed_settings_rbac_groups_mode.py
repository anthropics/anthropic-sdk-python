from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeCodeManagedSettingsRBACGroupsMode"]


class BetaClaudeCodeManagedSettingsRBACGroupsMode(BaseModel):
    type: Literal["rbac_groups"]
    """Always `rbac_groups`."""
