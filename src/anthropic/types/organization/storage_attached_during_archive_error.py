from typing_extensions import Literal

from ..._exceptions import ConflictError
from .storage_attached_during_archive_error_details import StorageAttachedDuringArchiveErrorDetails

__all__ = ["StorageAttachedDuringArchiveError"]


class StorageAttachedDuringArchiveError(ConflictError):
    """
    The Workspace was archived, but External Storage was attached to it during the archive and is still attached. To detach it, archive the Workspace again as a caller with the `org:external-storage:use` permission.
    """

    error_code: Literal["storage_attached_during_archive"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: StorageAttachedDuringArchiveErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
