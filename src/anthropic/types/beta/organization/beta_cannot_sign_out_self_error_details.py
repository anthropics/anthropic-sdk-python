from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaCannotSignOutSelfErrorDetails"]


class BetaCannotSignOutSelfErrorDetails(BaseModel):
    """The member is the user the API key or token belongs to."""

    error_code: Literal["cannot_sign_out_self"]
