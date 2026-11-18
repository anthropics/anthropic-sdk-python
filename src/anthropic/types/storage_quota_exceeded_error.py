from typing_extensions import Literal

from .._exceptions import BadRequestError
from .storage_quota_exceeded_error_details import StorageQuotaExceededErrorDetails

__all__ = ["StorageQuotaExceededError"]


class StorageQuotaExceededError(BadRequestError):
    """The organization's file storage quota is exhausted.

    Delete files to free up space, then retry the upload.
    """

    error_code: Literal["storage_quota_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: StorageQuotaExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
