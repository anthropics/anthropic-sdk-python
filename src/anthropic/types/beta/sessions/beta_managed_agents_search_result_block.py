# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_search_result_content import BetaManagedAgentsSearchResultContent
from .beta_managed_agents_search_result_citations import BetaManagedAgentsSearchResultCitations

__all__ = ["BetaManagedAgentsSearchResultBlock"]


class BetaManagedAgentsSearchResultBlock(BaseModel):
    """A block containing a web search result."""

    citations: BetaManagedAgentsSearchResultCitations
    """Citation settings for a search result."""

    content: List[BetaManagedAgentsSearchResultContent]
    """Array of text content blocks from the search result."""

    source: str
    """The URL source of the search result."""

    title: str
    """The title of the search result."""

    type: Literal["search_result"]
