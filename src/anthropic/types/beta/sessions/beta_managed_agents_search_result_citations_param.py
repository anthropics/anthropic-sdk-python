# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["BetaManagedAgentsSearchResultCitationsParam"]


class BetaManagedAgentsSearchResultCitationsParam(TypedDict, total=False):
    """Citation settings for a search result."""

    enabled: Required[bool]
    """Whether citations are enabled for this search result."""
