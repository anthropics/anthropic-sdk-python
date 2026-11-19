from typing_extensions import Literal

from ....._exceptions import NotFoundError
from .beta_rbac_group_managed_settings_not_found_error_details import BetaRBACGroupManagedSettingsNotFoundErrorDetails

__all__ = ["BetaRBACGroupManagedSettingsNotFoundError"]


class BetaRBACGroupManagedSettingsNotFoundError(NotFoundError):
    """This RBAC Group has no Claude Code managed settings."""

    error_code: Literal["rbac_group_managed_settings_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaRBACGroupManagedSettingsNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
