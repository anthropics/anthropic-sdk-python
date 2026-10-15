from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .model_line import ModelLine
from .model_capabilities import ModelCapabilities

__all__ = ["ModelInfo"]


class ModelInfo(BaseModel):
    id: str
    """Unique model identifier."""

    capabilities: Optional[ModelCapabilities] = None
    """Object mapping capability names to their support details.

    Keys are always present for all known capabilities.
    """

    created_at: datetime
    """RFC 3339 datetime string representing the time at which the model was released.

    May be set to an epoch value if the release date is unknown.
    """

    deprecated_at: Optional[datetime] = None
    """
    RFC 3339 datetime string representing the time of the model's most recent
    deprecation. Populated for `deprecated` and `retired` models; `null` while the
    model is `active`.
    """

    display_name: str
    """A human-readable name for the model."""

    lifecycle: Literal["active", "deprecated", "retired"]
    """The model's current lifecycle stage.

    - `active`: The model is available for use, open to new adopters, and not
      scheduled for retirement.
    - `deprecated`: The model remains callable for organizations with existing
      access, but is headed for retirement and closed to new adopters.
    - `retired`: The model is no longer available for use; inference requests naming
      it fail. It remains in the catalogue as the historical record of its
      retirement.
    """

    line: Optional[ModelLine] = None
    """
    The model line this model belongs to, such as `opus` for both Claude Opus 4.5
    and Claude Opus 4.6. More lines may be added. `null` when the model belongs to
    no line; do not infer a line from the `id`.
    """

    max_input_tokens: Optional[int] = None
    """Maximum input context window size in tokens for this model."""

    max_tokens: Optional[int] = None
    """Maximum value for the `max_tokens` parameter when using this model."""

    retires_at: Optional[datetime] = None
    """
    RFC 3339 datetime string representing the model's currently scheduled retirement
    date. The schedule can be revised until retirement occurs; `null` while the
    model is `active` or while no retirement is scheduled. A past date on a
    `deprecated` model means retirement is overdue, not that it has occurred:
    `lifecycle` is the retirement signal.
    """

    type: Literal["model"]
    """Object type.

    For Models, this is always `"model"`.
    """
