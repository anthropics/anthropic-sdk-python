from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaUnsupportedRegionErrorDetails"]


class BetaUnsupportedRegionErrorDetails(BaseModel):
    """`provider_config.region` is not a region where External Storage is available."""

    error_code: Literal["unsupported_region"]
