# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_span_model_usage import BetaManagedAgentsSpanModelUsage

__all__ = ["BetaManagedAgentsSpanOutcomeEvaluationEndEvent"]


class BetaManagedAgentsSpanOutcomeEvaluationEndEvent(BaseModel):
    """Emitted when an outcome evaluation cycle completes.

    Carries the verdict and aggregate token usage. A verdict of `needs_revision` means another evaluation cycle follows; `satisfied`, `max_iterations_reached`, `failed`, or `interrupted` are terminal — no further evaluation cycles follow.
    """

    id: str
    """Unique identifier for this event."""

    explanation: str
    """Human-readable explanation of the verdict.

    For `needs_revision`, describes which criteria failed and why.
    """

    iteration: int
    """
    0-indexed revision cycle, matching the corresponding
    `span.outcome_evaluation_start`.
    """

    outcome_evaluation_start_id: str
    """The id of the corresponding `span.outcome_evaluation_start` event."""

    outcome_id: str
    """The `outc_` ID of the outcome being evaluated."""

    processed_at: datetime
    """A timestamp in RFC 3339 format"""

    result: str
    """Evaluation verdict.

    'satisfied': criteria met, session goes idle. 'needs_revision': criteria not
    met, another revision cycle follows. 'max_iterations_reached': evaluation budget
    exhausted with criteria still unmet — one final acknowledgment turn follows
    before the session goes idle, but no further evaluation runs. 'failed': grader
    determined the rubric does not apply to the deliverables. 'interrupted': user
    sent an interrupt while evaluation was in progress.
    """

    type: Literal["span.outcome_evaluation_end"]

    usage: BetaManagedAgentsSpanModelUsage
    """Token usage for a single model request."""
