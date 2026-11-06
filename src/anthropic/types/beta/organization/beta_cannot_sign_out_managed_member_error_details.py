from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutManagedMemberErrorDetails"]


class BetaCannotSignOutManagedMemberErrorDetails(BaseModel):
    """
    The member has the `managed` role, and this API key or token cannot sign them out. The error message says which keys and tokens can.
    """

    error_code: Literal["cannot_sign_out_managed_member"]
