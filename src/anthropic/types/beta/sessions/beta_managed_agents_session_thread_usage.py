from typing import Optional

from ...._models import BaseModel
from ...beta_monetary_amount import BetaMonetaryAmount
from ..beta_managed_agents_server_tool_usage import BetaManagedAgentsServerToolUsage
from ..beta_managed_agents_cache_creation_usage import BetaManagedAgentsCacheCreationUsage

__all__ = ["BetaManagedAgentsSessionThreadUsage"]


class BetaManagedAgentsSessionThreadUsage(BaseModel):
    """Cumulative token usage for a session thread across all turns."""

    active_seconds: Optional[float] = None
    """Cumulative time in seconds this thread spent in running status.

    Equal to `stats.active_seconds`; surfaced here so a thread's usage carries every
    quantity its cost is priced on.
    """

    cache_creation: Optional[BetaManagedAgentsCacheCreationUsage] = None
    """Tokens used to create prompt cache entries, broken down by cache TTL."""

    cache_read_input_tokens: Optional[int] = None
    """Total tokens read from prompt cache."""

    input_tokens: Optional[int] = None
    """Total input tokens consumed across all turns."""

    list_cost: Optional[BetaMonetaryAmount] = None
    """
    Cumulative list cost of this thread across all turns, priced at public list
    rates. Absent until cost tracking is available for the thread. Each figure is
    rounded to the nearest cent independently and the session's aggregate
    `usage.list_cost` additionally includes session runtime, so per-thread costs do
    not sum exactly to the session figure; the session figure is authoritative and
    is what a budget is enforced against.
    """

    output_tokens: Optional[int] = None
    """Total output tokens generated across all turns."""

    server_tool_use: Optional[BetaManagedAgentsServerToolUsage] = None
    """Cumulative server-executed tool usage across all turns of this thread.

    Absent until server-tool tracking is available for the thread.
    """
