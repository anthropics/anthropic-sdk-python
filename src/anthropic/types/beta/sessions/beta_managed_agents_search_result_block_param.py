# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .beta_managed_agents_search_result_content_param import BetaManagedAgentsSearchResultContentParam
from .beta_managed_agents_search_result_citations_param import BetaManagedAgentsSearchResultCitationsParam

__all__ = ["BetaManagedAgentsSearchResultBlockParam"]


class BetaManagedAgentsSearchResultBlockParam(TypedDict, total=False):
    """A block containing a web search result."""

    citations: Required[BetaManagedAgentsSearchResultCitationsParam]
    """Citation settings for a search result."""

    content: Required[Iterable[BetaManagedAgentsSearchResultContentParam]]
    """Array of text content blocks from the search result."""

    source: Required[str]
    """The URL source of the search result."""

    title: Required[str]
    """The title of the search result."""

    type: Required[Literal["search_result"]]
