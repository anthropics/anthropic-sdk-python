# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

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
    """Prompt-cache creation token usage broken down by cache lifetime."""

    cache_read_input_tokens: Optional[int] = None
    """Total tokens read from prompt cache."""

    input_tokens: Optional[int] = None
    """Total input tokens consumed across all turns."""

    list_cost: Optional[BetaMonetaryAmount] = None
    """A monetary amount in a specific currency."""

    output_tokens: Optional[int] = None
    """Total output tokens generated across all turns."""

    server_tool_use: Optional[BetaManagedAgentsServerToolUsage] = None
    """Cumulative count of server-executed tool invocations, broken down by tool."""
