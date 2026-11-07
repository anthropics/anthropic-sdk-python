from typing import Optional

from ...._models import BaseModel
from ...beta_monetary_amount import BetaMonetaryAmount
from ..beta_managed_agents_server_tool_usage import BetaManagedAgentsServerToolUsage
from ..beta_managed_agents_cache_creation_usage import BetaManagedAgentsCacheCreationUsage

__all__ = ["BetaManagedAgentsSessionUsageSnapshot"]


class BetaManagedAgentsSessionUsageSnapshot(BaseModel):
    """Point-in-time snapshot of a session's cumulative usage."""

    active_seconds: Optional[float] = None
    """
    Cumulative time in seconds during which the session had at least one thread in
    running status. Overlapping activity from concurrent threads is counted once.
    This is the duration the session's runtime cost is priced on.
    """

    cache_creation: Optional[BetaManagedAgentsCacheCreationUsage] = None
    """Tokens used to create prompt cache entries, broken down by cache TTL."""

    cache_read_input_tokens: Optional[int] = None
    """Total tokens read from prompt cache."""

    input_tokens: Optional[int] = None
    """Total input tokens consumed across all turns."""

    list_cost: Optional[BetaMonetaryAmount] = None
    """
    Cumulative list cost of the session across all turns, priced at public list
    rates.
    """

    output_tokens: Optional[int] = None
    """Total output tokens generated across all turns."""

    server_tool_use: Optional[BetaManagedAgentsServerToolUsage] = None
    """Cumulative server-executed tool usage across all turns."""
