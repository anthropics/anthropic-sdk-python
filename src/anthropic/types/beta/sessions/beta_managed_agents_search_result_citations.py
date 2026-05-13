# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSearchResultCitations"]


class BetaManagedAgentsSearchResultCitations(BaseModel):
    """Citation settings for a search result."""

    enabled: bool
    """Whether citations are enabled for this search result."""
