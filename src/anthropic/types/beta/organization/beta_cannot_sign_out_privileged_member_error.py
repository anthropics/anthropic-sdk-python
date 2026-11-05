from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_cannot_sign_out_privileged_member_error_details import BetaCannotSignOutPrivilegedMemberErrorDetails

__all__ = ["BetaCannotSignOutPrivilegedMemberError"]


class BetaCannotSignOutPrivilegedMemberError(PermissionDeniedError):
    """
    This OAuth token cannot sign out a membership admin or a member whose roles grant owner, user management, or identity and access management.
    """

    error_code: Literal["cannot_sign_out_privileged_member"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutPrivilegedMemberErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
