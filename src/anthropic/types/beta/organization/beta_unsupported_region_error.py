from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_unsupported_region_error_details import BetaUnsupportedRegionErrorDetails

__all__ = ["BetaUnsupportedRegionError"]


class BetaUnsupportedRegionError(BadRequestError):
    """`provider_config.region` is not a region where External Storage is available."""

    error_code: Literal["unsupported_region"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaUnsupportedRegionErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
