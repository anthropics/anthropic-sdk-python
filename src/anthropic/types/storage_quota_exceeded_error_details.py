from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["StorageQuotaExceededErrorDetails"]


class StorageQuotaExceededErrorDetails(BaseModel):
    """The organization's file storage quota is exhausted.

    Delete files to free up space, then retry the upload.
    """

    error_code: Literal["storage_quota_exceeded"]
