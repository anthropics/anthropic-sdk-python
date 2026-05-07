# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsOutcomeEvaluationResource"]


class BetaManagedAgentsOutcomeEvaluationResource(BaseModel):
    """Evaluation state for a single outcome defined via a define_outcome event."""

    completed_at: Optional[datetime] = None
    """A timestamp in RFC 3339 format"""

    description: str
    """What the agent should produce."""

    explanation: Optional[str] = None
    """Grader's verdict text from the most recent evaluation.

    For satisfied, explains why criteria are met; for needs_revision (intermediate),
    what's missing; for failed, why unrecoverable.
    """

    iteration: int
    """0-indexed revision cycle the outcome is currently on."""

    outcome_id: str
    """Server-generated outc\\__ ID for this outcome."""

    result: str
    """Current evaluation state.

    'pending' before the agent begins work; 'running' while producing or revising;
    'evaluating' while the grader scores;
    'satisfied'/'max_iterations_reached'/'failed'/'interrupted' are terminal.
    """

    type: Literal["outcome_evaluation"]
