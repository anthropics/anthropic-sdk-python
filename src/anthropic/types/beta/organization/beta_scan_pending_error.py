from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_scan_pending_error_details import BetaScanPendingErrorDetails

__all__ = ["BetaScanPendingError"]


class BetaScanPendingError(ConflictError):
    """The content scan of the version in `plugin_version_id` is still running.

    Retry once the scan finishes.
    """

    error_code: Literal["scan_pending"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaScanPendingErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
