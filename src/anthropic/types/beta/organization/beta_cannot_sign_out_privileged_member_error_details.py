from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutPrivilegedMemberErrorDetails"]


class BetaCannotSignOutPrivilegedMemberErrorDetails(BaseModel):
    """
    This OAuth token cannot sign out a membership admin or a member whose roles grant owner, user management, or identity and access management.
    """

    error_code: Literal["cannot_sign_out_privileged_member"]
