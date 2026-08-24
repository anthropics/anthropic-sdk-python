# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsUserLocationParam"]


class BetaManagedAgentsUserLocationParam(TypedDict, total=False):
    """Approximate user location for search result localization."""

    type: Required[Literal["approximate"]]
    """Location precision. Only "approximate" is supported."""

    city: Optional[str]
    """City name."""

    country: Optional[str]
    """Two-letter ISO 3166-1 country code, uppercase."""

    region: Optional[str]
    """Region or state name."""

    timezone: Optional[str]
    """IANA timezone identifier, e.g. "America/Los_Angeles"."""
