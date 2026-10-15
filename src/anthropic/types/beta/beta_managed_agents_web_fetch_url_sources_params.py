from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .beta_managed_agents_web_fetch_url_source_user_input_params import (
    BetaManagedAgentsWebFetchURLSourceUserInputParams,
)
from .beta_managed_agents_web_fetch_url_source_tool_filter_params import (
    BetaManagedAgentsWebFetchURLSourceToolFilterParams,
)

__all__ = ["BetaManagedAgentsWebFetchURLSourcesParams"]


class BetaManagedAgentsWebFetchURLSourcesParams(TypedDict, total=False):
    """Which sources contribute URLs the web_fetch tool may fetch.

    When web_fetch is limited to URLs the conversation has already shown the model (in a user message, a custom tool's result, or an earlier web_search or web_fetch result), each key narrows one of those sources and defaults to "all". Setting all three keys to "none" is rejected.
    """

    client_tool_results: Optional[BetaManagedAgentsWebFetchURLSourceToolFilterParams]
    """
    Which custom tools' results contribute URLs that may be fetched: "all" (the
    default), "none", or an only or except list. Each name in a list must be a
    custom tool in the same tools array.
    """

    server_tool_results: Optional[BetaManagedAgentsWebFetchURLSourceToolFilterParams]
    """
    Which of the web_search and web_fetch tools' results contribute URLs that may be
    fetched: "all" (the default), "none", or an only or except list. Each name in a
    list must be "web_search" or "web_fetch".
    """

    user_input: Optional[BetaManagedAgentsWebFetchURLSourceUserInputParams]
    """
    Whether URLs in the text of user messages may be fetched: "all" (the default) or
    "none".
    """
