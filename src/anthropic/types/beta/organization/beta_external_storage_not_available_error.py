from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_external_storage_not_available_error_details import BetaExternalStorageNotAvailableErrorDetails

__all__ = ["BetaExternalStorageNotAvailableError"]


class BetaExternalStorageNotAvailableError(BadRequestError):
    """
    External Storage isn't available for this Workspace, so only `internal` storage is accepted. The error's `message` says why.
    """

    error_code: Literal["external_storage_not_available"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaExternalStorageNotAvailableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
