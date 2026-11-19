from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_claude_code_managed_settings_mode import BetaClaudeCodeManagedSettingsMode

__all__ = ["BetaClaudeCodeManagedSettingsConfiguration"]


class BetaClaudeCodeManagedSettingsConfiguration(BaseModel):
    mode: BetaClaudeCodeManagedSettingsMode
    """How the organization serves managed settings.

    In `organization` mode every member receives the organization settings, which
    are set in claude.ai. In `rbac_groups` mode each member receives the settings of
    the first RBAC Group in `rbac_group_order` that they belong to. A member in none
    of them receives the default settings, or no settings if no default is set.
    """

    mode_updated_at: Optional[datetime] = None
    """When the mode last changed, in RFC 3339 format, or `null` if it never has."""

    rbac_group_order: List[str]
    """
    The ID of every RBAC Group with settings, deleted groups included, highest
    precedence first.
    """

    rbac_group_order_version: str
    """An opaque version of `rbac_group_order`, which changes whenever the order does.

    Send it back with a new order.
    """

    type: Literal["claude_code_managed_settings_configuration"]
    """Always `claude_code_managed_settings_configuration`."""
