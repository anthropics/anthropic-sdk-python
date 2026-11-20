from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_storage_changed_concurrently_error_details import BetaStorageChangedConcurrentlyErrorDetails

__all__ = ["BetaStorageChangedConcurrentlyError"]


class BetaStorageChangedConcurrentlyError(ConflictError):
    """
    Another request changed this storage setting while this one was running, so this request left it as it is. Read the Workspace and send the request again if you still want the change.
    """

    error_code: Literal["storage_changed_concurrently"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaStorageChangedConcurrentlyErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
