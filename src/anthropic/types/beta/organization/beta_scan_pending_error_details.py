from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaScanPendingErrorDetails"]


class BetaScanPendingErrorDetails(BaseModel):
    """The content scan of the version in `plugin_version_id` is still running.

    Retry once the scan finishes.
    """

    error_code: Literal["scan_pending"]

    plugin_version_id: str
