from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["FileExpiredErrorDetails"]


class FileExpiredErrorDetails(BaseModel):
    """The file's `expires_at` has passed, so its content is no longer available."""

    error_code: Literal["file_expired"]
