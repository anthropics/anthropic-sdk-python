# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSpanOutcomeEvaluationStartEvent"]


class BetaManagedAgentsSpanOutcomeEvaluationStartEvent(BaseModel):
    """Emitted when an outcome evaluation cycle begins."""

    id: str
    """Unique identifier for this event."""

    iteration: int
    """0-indexed revision cycle.

    0 is the first evaluation; 1 is the re-evaluation after the first revision; etc.
    """

    outcome_id: str
    """The `outc_` ID of the outcome being evaluated."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["span.outcome_evaluation_start"]
