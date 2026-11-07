from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaUserLocation"]


class BetaUserLocation(BaseModel):
    type: Literal["approximate"]

    city: Optional[str] = None
    """The city of the user."""

    country: Optional[str] = None
    """
    The two letter
    [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) of the
    user.
    """

    region: Optional[str] = None
    """The region of the user."""

    timezone: Optional[str] = None
    """The [IANA timezone](https://nodatime.org/TimeZones) of the user."""
