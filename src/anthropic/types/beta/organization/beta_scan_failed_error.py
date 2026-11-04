from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_scan_failed_error_details import BetaScanFailedErrorDetails

__all__ = ["BetaScanFailedError"]


class BetaScanFailedError(BadRequestError):
    """
    The content scan of the version in `plugin_version_id` failed, errored or reached no verdict, so the version cannot be served.
    """

    error_code: Literal["scan_failed"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaScanFailedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
