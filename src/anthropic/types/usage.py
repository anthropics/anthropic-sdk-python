# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .cache_creation import CacheCreation
from .server_tool_usage import ServerToolUsage
from .output_tokens_details import OutputTokensDetails

__all__ = ["Usage"]


class Usage(BaseModel):
    cache_creation: Optional[CacheCreation] = None
    """Breakdown of cached tokens by TTL"""

    cache_creation_input_tokens: Optional[int] = None
    """The number of input tokens used to create the cache entry."""

    cache_read_input_tokens: Optional[int] = None
    """The number of input tokens read from the cache."""

    inference_geo: Optional[str] = None
    """The geographic region where inference was performed for this request."""

    input_tokens: int
    """The number of input tokens which were used."""

    output_tokens: int
    """The number of output tokens which were used."""

    output_tokens_details: Optional[OutputTokensDetails] = None
    """Breakdown of output tokens by category.

    `output_tokens` remains the inclusive, authoritative total used for billing.
    This object provides a read-only decomposition for observability — for example,
    how many of the billed output tokens were spent on internal reasoning that may
    have been summarized before being returned to you.
    """

    server_tool_use: Optional[ServerToolUsage] = None
    """The number of server tool requests."""

    service_tier: Optional[Literal["standard", "priority", "batch"]] = None
    """If the request used the priority, standard, or batch tier."""
