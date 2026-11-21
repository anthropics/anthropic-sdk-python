from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel
from .beta_claude_code_rbac_group_status import BetaClaudeCodeRBACGroupStatus

__all__ = ["BetaClaudeCodeRBACGroupManagedSettingsSummary"]


class BetaClaudeCodeRBACGroupManagedSettingsSummary(BaseModel):
    created_at: datetime
    """When the settings document this group uses was first stored, in RFC 3339 format.

    This can be earlier than when the group got its settings, and it changes if the
    group gets a different document.
    """

    rbac_group_id: str
    """The RBAC Group's ID, prefixed `rbac_group_`."""

    rbac_group_status: BetaClaudeCodeRBACGroupStatus
    """Whether the group is still one of the organization's RBAC Groups.

    Its `type` is `active` if it is, `deleted` if it is not, and `unknown` if that
    cannot be checked right now. A deleted group's settings stay in
    `rbac_group_order` but match no member.
    """

    type: Literal["claude_code_rbac_group_managed_settings_summary"]
    """Always `claude_code_rbac_group_managed_settings_summary`."""

    updated_at: datetime
    """
    When this group's settings or its position in the order last changed, in RFC
    3339 format. Its position changes whenever the number of groups ahead of it
    changes.
    """
