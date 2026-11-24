from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_gcp_project_not_verified_error_details import BetaGCPProjectNotVerifiedErrorDetails

__all__ = ["BetaGCPProjectNotVerifiedError"]


class BetaGCPProjectNotVerifiedError(BadRequestError):
    """
    The organization has not proved that it owns the Google Cloud project that holds the key or bucket. The message names the field.
    """

    error_code: Literal["gcp_project_not_verified"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaGCPProjectNotVerifiedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
