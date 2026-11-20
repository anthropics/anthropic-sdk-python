from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_storage_verification_failed_error_details import BetaStorageVerificationFailedErrorDetails

__all__ = ["BetaStorageVerificationFailedError"]


class BetaStorageVerificationFailedError(BadRequestError):
    """The External Storage failed verification, so the request changed nothing.

    `failed_checks` lists what to fix.
    """

    error_code: Literal["storage_verification_failed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageVerificationFailedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
