from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_cannot_sign_out_membership_admin_error_details import BetaCannotSignOutMembershipAdminErrorDetails

__all__ = ["BetaCannotSignOutMembershipAdminError"]


class BetaCannotSignOutMembershipAdminError(PermissionDeniedError):
    """
    The member is a membership admin, and the person the API key or token belongs to is not allowed to sign out membership admins.
    """

    error_code: Literal["cannot_sign_out_membership_admin"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutMembershipAdminErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
