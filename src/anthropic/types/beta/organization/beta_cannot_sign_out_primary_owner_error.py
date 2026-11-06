from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_cannot_sign_out_primary_owner_error_details import BetaCannotSignOutPrimaryOwnerErrorDetails

__all__ = ["BetaCannotSignOutPrimaryOwnerError"]


class BetaCannotSignOutPrimaryOwnerError(BadRequestError):
    """
    The member is the organization's primary owner, whom no API key or token can sign out.
    """

    error_code: Literal["cannot_sign_out_primary_owner"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutPrimaryOwnerErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
