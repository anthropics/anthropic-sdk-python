from typing import Optional
from typing_extensions import Literal

from ..model import Model
from ..._models import BaseModel
from .beta_cache_creation import BetaCacheCreation

__all__ = ["BetaFallbackMessageIterationUsage"]


class BetaFallbackMessageIterationUsage(BaseModel):
    """Token usage for the fallback-model attempt of a server-side fallback request.

    The terminal entry of a fallback-served turn: when a fallback hop's
    output is the returned message, the entry for the iteration that
    completed it carries this type in place of `message`. A declined hop
    and the serving hop's earlier tool-loop iterations produce `message`
    entries. Whether a fallback model served the response is signalled by
    the presence of this entry in `usage.iterations`.
    """

    cache_creation: Optional[BetaCacheCreation] = None
    """Breakdown of cached tokens by TTL"""

    cache_creation_input_tokens: int
    """The number of input tokens used to create the cache entry."""

    cache_read_input_tokens: int
    """The number of input tokens read from the cache."""

    input_tokens: int
    """The number of input tokens which were used."""

    model: Model
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """

    output_tokens: int
    """The number of output tokens which were used."""

    type: Literal["fallback_message"]
    """Usage for the fallback-model attempt that served the response"""
