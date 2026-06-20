# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..model import Model
from ..._models import BaseModel

__all__ = ["BetaFallbackInfo"]


class BetaFallbackInfo(BaseModel):
    """Identifies one hop of a fallback transition."""

    model: Model
    """The model that will complete your prompt.

    See [models](https://docs.anthropic.com/en/docs/models-overview) for additional
    details and options.
    """
