# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_model_capabilities import BetaModelCapabilities

__all__ = ["BetaModelInfo"]


class BetaModelInfo(BaseModel):
    id: str
    """Unique model identifier."""

    allowed_fallback_models: Optional[List[str]] = None
    """Model IDs this model accepts as `fallbacks[i].model` on the Messages API.

    An empty list means the `fallbacks` parameter is not supported for this model as
    primary.
    """

    capabilities: Optional[BetaModelCapabilities] = None
    """Model capability information."""

    created_at: datetime
    """RFC 3339 datetime string representing the time at which the model was released.

    May be set to an epoch value if the release date is unknown.
    """

    display_name: str
    """A human-readable name for the model."""

    max_input_tokens: Optional[int] = None
    """Maximum input context window size in tokens for this model."""

    max_tokens: Optional[int] = None
    """Maximum value for the `max_tokens` parameter when using this model."""

    type: Literal["model"]
    """Object type.

    For Models, this is always `"model"`.
    """
