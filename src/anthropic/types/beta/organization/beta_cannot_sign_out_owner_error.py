from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_cannot_sign_out_owner_error_details import BetaCannotSignOutOwnerErrorDetails

__all__ = ["BetaCannotSignOutOwnerError"]


class BetaCannotSignOutOwnerError(PermissionDeniedError):
    """
    The member is an owner or has owner permissions, and this API key or token cannot sign them out. In a Claude Enterprise organization, an API key with the `write:members` scope can.
    """

    error_code: Literal["cannot_sign_out_owner"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutOwnerErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
