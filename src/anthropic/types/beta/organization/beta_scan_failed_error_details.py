from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaScanFailedErrorDetails"]


class BetaScanFailedErrorDetails(BaseModel):
    """
    The version in `plugin_version_id` did not pass its content scan, so it cannot be served.
    """

    error_code: Literal["scan_failed"]

    plugin_version_id: str
