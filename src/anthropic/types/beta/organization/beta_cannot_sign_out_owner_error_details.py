from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutOwnerErrorDetails"]


class BetaCannotSignOutOwnerErrorDetails(BaseModel):
    """
    The member is an owner or has owner permissions, and this API key or token cannot sign them out. In a Claude Enterprise organization, an API key with the `write:members` scope can.
    """

    error_code: Literal["cannot_sign_out_owner"]
