from typing import Optional

from ....._models import BaseModel
from ...beta_cache_creation import BetaCacheCreation
from ..beta_analytics_server_tool_use import BetaAnalyticsServerToolUse

__all__ = ["BetaAnalyticsUsageMetrics"]


class BetaAnalyticsUsageMetrics(BaseModel):
    """The token usage of one row."""

    cache_creation: BetaCacheCreation
    """The number of input tokens for cache creation."""

    cache_read_input_tokens: int
    """The number of input tokens read from the cache."""

    output_tokens: int
    """The number of output tokens generated."""

    requests: Optional[int] = None
    """Number of API requests in this row's scope.

    For sandbox / code-execution events, this counts execution spans rather than
    HTTP requests (these rows surface with `product: null`).
    """

    server_tool_use: BetaAnalyticsServerToolUse
    """Server-side tool usage metrics."""

    total_tokens: int
    """Total token count across all token types.

    This is the value the default `order_by` (`total_tokens`) sorts on.
    """

    uncached_input_tokens: int
    """The number of uncached input tokens processed."""
