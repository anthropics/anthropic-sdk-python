from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_spend_limits_admin_api_writes_not_enabled_error_details import (
    BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails,
)

__all__ = ["BetaSpendLimitsAdminAPIWritesNotEnabledError"]


class BetaSpendLimitsAdminAPIWritesNotEnabledError(PermissionDeniedError):
    """
    The organization cannot retrieve, set or delete spend limits with an Admin API credential.
    """

    error_code: Literal["spend_limits_admin_api_writes_not_enabled"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
