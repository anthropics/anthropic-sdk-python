from typing_extensions import Literal

from .._exceptions import ConflictError
from .beta_storage_in_use_error_details import BetaStorageInUseErrorDetails

__all__ = ["BetaStorageInUseError"]


class BetaStorageInUseError(ConflictError):
    """The bucket is already in use, or was in use recently. Name a different bucket."""

    error_code: Literal["storage_in_use"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageInUseErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
