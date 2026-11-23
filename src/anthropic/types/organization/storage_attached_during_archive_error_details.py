from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["StorageAttachedDuringArchiveErrorDetails"]


class StorageAttachedDuringArchiveErrorDetails(BaseModel):
    """
    The Workspace was archived, but External Storage was attached to it during the archive and is still attached. To detach it, archive the Workspace again as a caller with the `org:external-storage:use` permission.
    """

    error_code: Literal["storage_attached_during_archive"]
