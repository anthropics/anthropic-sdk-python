from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_cannot_sign_out_self_error_details import BetaCannotSignOutSelfErrorDetails

__all__ = ["BetaCannotSignOutSelfError"]


class BetaCannotSignOutSelfError(BadRequestError):
    """The member is the user the API key or token belongs to."""

    error_code: Literal["cannot_sign_out_self"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaCannotSignOutSelfErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
