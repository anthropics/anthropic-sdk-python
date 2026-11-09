from typing_extensions import Literal

from ...._exceptions import PermissionDeniedError
from .beta_cannot_sign_out_managed_member_error_details import BetaCannotSignOutManagedMemberErrorDetails

__all__ = ["BetaCannotSignOutManagedMemberError"]


class BetaCannotSignOutManagedMemberError(PermissionDeniedError):
    """
    On a public-sector deployment, only an API key or token that belongs to a person with owner permissions can sign out a member with the `managed` role.
    """

    error_code: Literal["cannot_sign_out_managed_member"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutManagedMemberErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
