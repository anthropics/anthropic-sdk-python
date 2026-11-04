from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_scan_failed_error_details import BetaScanFailedErrorDetails

__all__ = ["BetaScanFailedError"]


class BetaScanFailedError(BadRequestError):
    """
    The version in `plugin_version_id` did not pass its content scan, so it cannot be served.
    """

    error_code: Literal["scan_failed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaScanFailedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
