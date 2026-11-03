from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaScanFailedErrorDetails"]


class BetaScanFailedErrorDetails(BaseModel):
    """
    The content scan of the version in `plugin_version_id` failed, errored or reached no verdict, so the version cannot be served.
    """

    error_code: Literal["scan_failed"]

    plugin_version_id: str
