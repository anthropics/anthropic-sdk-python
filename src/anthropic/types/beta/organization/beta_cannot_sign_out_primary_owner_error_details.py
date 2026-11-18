from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutPrimaryOwnerErrorDetails"]


class BetaCannotSignOutPrimaryOwnerErrorDetails(BaseModel):
    """
    The member is the organization's primary owner, whom no API key or token can sign out.
    """

    error_code: Literal["cannot_sign_out_primary_owner"]
