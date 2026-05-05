# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSpanOutcomeEvaluationOngoingEvent"]


class BetaManagedAgentsSpanOutcomeEvaluationOngoingEvent(BaseModel):
    """Periodic heartbeat emitted while an outcome evaluation cycle is in progress.

    Distinguishes 'evaluation is actively running' from 'evaluation is stuck' between the corresponding `span.outcome_evaluation_start` and `span.outcome_evaluation_end` events.
    """

    id: str
    """Unique identifier for this event."""

    iteration: int
    """
    0-indexed revision cycle, matching the corresponding
    `span.outcome_evaluation_start`.
    """

    outcome_id: str
    """The `outc_` ID of the outcome being evaluated."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    type: Literal["span.outcome_evaluation_ongoing"]
