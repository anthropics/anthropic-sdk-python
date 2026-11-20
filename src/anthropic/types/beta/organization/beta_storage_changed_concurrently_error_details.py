from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaStorageChangedConcurrentlyErrorDetails"]


class BetaStorageChangedConcurrentlyErrorDetails(BaseModel):
    """
    Another request changed this storage setting while this one was running, so this request left it as it is. Read the Workspace and send the request again if you still want the change.
    """

    error_code: Literal["storage_changed_concurrently"]

    field: str
    """The storage setting that changed."""
