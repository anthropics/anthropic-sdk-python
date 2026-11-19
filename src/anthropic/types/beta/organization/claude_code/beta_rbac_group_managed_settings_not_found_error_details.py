from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaRBACGroupManagedSettingsNotFoundErrorDetails"]


class BetaRBACGroupManagedSettingsNotFoundErrorDetails(BaseModel):
    """This RBAC Group has no Claude Code managed settings."""

    error_code: Literal["rbac_group_managed_settings_not_found"]
