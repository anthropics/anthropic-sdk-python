from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_external_storage_in_use_error_details import BetaExternalStorageInUseErrorDetails

__all__ = ["BetaExternalStorageInUseError"]


class BetaExternalStorageInUseError(BadRequestError):
    """The External Storage is `active` or `draining`, so this delete didn't erase it.

    The message says what to do next. On `draining` storage this delete may have started a removal that can't be undone: get the storage and read `status.removal_started`.
    """

    error_code: Literal["external_storage_in_use"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaExternalStorageInUseErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
