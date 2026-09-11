from ..._models import BaseModel

__all__ = ["BetaServerToolUsage"]


class BetaServerToolUsage(BaseModel):
    web_fetch_requests: int
    """The number of web fetch tool requests."""

    web_search_requests: int
    """The number of web search tool requests."""
