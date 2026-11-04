from typing_extensions import Literal

from .._exceptions import NotFoundError
from .file_expired_error_details import FileExpiredErrorDetails

__all__ = ["FileExpiredError"]


class FileExpiredError(NotFoundError):
    """The file's `expires_at` has passed, so its content is no longer available."""

    error_code: Literal["file_expired"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: FileExpiredErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
