from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BetaRegionNotSupportedErrorDetails"]


class BetaRegionNotSupportedErrorDetails(BaseModel):
    """
    The request names a region code that the control does not take from this organization. The message names the field.
    """

    error_code: Literal["region_not_supported"]
