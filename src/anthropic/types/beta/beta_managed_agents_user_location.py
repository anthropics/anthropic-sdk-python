# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsUserLocation"]


class BetaManagedAgentsUserLocation(BaseModel):
    """Approximate user location for search result localization."""

    type: Literal["approximate"]
    """Location precision. Only "approximate" is supported."""

    city: Optional[str] = None
    """City name."""

    country: Optional[str] = None
    """Two-letter ISO 3166-1 country code, uppercase."""

    region: Optional[str] = None
    """Region or state name."""

    timezone: Optional[str] = None
    """IANA timezone identifier, e.g. "America/Los_Angeles"."""
