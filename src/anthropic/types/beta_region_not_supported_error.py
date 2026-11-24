from typing_extensions import Literal

from .._exceptions import BadRequestError
from .beta_region_not_supported_error_details import BetaRegionNotSupportedErrorDetails

__all__ = ["BetaRegionNotSupportedError"]


class BetaRegionNotSupportedError(BadRequestError):
    """
    The request names a region code that the control does not take from this organization. The message names the field.
    """

    error_code: Literal["region_not_supported"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaRegionNotSupportedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
