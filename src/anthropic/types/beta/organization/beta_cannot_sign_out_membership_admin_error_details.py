from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutMembershipAdminErrorDetails"]


class BetaCannotSignOutMembershipAdminErrorDetails(BaseModel):
    """
    The member is a membership admin, and the person the API key or token belongs to is not allowed to sign out membership admins.
    """

    error_code: Literal["cannot_sign_out_membership_admin"]
