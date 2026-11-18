from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_cannot_sign_out_managed_member_error_details import BetaCannotSignOutManagedMemberErrorDetails

__all__ = ["BetaCannotSignOutManagedMemberError"]


class BetaCannotSignOutManagedMemberError(PermissionDeniedError):
    """
    The member has the `managed` role, and this API key or token cannot sign them out. The error message says which keys and tokens can.
    """

    error_code: Literal["cannot_sign_out_managed_member"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutManagedMemberErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
