# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsServerToolUsage"]


class BetaManagedAgentsServerToolUsage(BaseModel):
    """Cumulative count of server-executed tool invocations, broken down by tool."""

    web_fetch_requests: Optional[int] = None
    """Number of server-executed web fetch requests."""

    web_search_requests: Optional[int] = None
    """Number of server-executed web search requests."""
