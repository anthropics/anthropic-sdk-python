# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["BetaDreamUsage"]


class BetaDreamUsage(BaseModel):
    """Cumulative token usage for the dream across every pipeline stage."""

    cache_creation_input_tokens: int
    """Total tokens used to create prompt-cache entries (sum of all TTL tiers)."""

    cache_read_input_tokens: int
    """Total tokens read from prompt cache."""

    input_tokens: int
    """Total uncached input tokens consumed across every pipeline stage."""

    output_tokens: int
    """Total output tokens generated across every pipeline stage."""
