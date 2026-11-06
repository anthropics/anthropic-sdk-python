from typing_extensions import Literal

from ..._exceptions import PermissionDeniedError
from .beta_billing_frozen_error_details import BetaBillingFrozenErrorDetails

__all__ = ["BetaBillingFrozenError"]


class BetaBillingFrozenError(PermissionDeniedError):
    """
    Anthropic has temporarily disabled billing changes for the user account the credential belongs to. Contact support.
    """

    error_code: Literal["billing_frozen"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaBillingFrozenErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
