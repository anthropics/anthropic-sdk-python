from ...._models import BaseModel

__all__ = ["BetaAnalyticsServerToolUse"]


class BetaAnalyticsServerToolUse(BaseModel):
    web_search_requests: int
    """The number of web search requests made."""
