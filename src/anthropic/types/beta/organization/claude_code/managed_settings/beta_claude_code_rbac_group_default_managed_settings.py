from typing import Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeCodeRBACGroupDefaultManagedSettings"]


class BetaClaudeCodeRBACGroupDefaultManagedSettings(BaseModel):
    settings: Optional[Dict[str, object]] = None
    """
    The default settings document, or `null` if none are set or the stored document
    is damaged and can no longer be read. To tell these apart, `updated_at` is
    `null` only when none are set. Replacing a damaged document fixes this.
    """

    type: Literal["claude_code_rbac_group_default_managed_settings"]
    """Always `claude_code_rbac_group_default_managed_settings`."""

    updated_at: Optional[datetime] = None
    """
    When the default settings last changed, in RFC 3339 format, or `null` if none
    are set.
    """
