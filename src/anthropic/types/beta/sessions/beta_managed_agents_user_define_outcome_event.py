from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_file_rubric import BetaManagedAgentsFileRubric
from .beta_managed_agents_text_rubric import BetaManagedAgentsTextRubric

__all__ = ["BetaManagedAgentsUserDefineOutcomeEvent", "Rubric"]

Rubric: TypeAlias = Annotated[
    Union[BetaManagedAgentsFileRubric, BetaManagedAgentsTextRubric], UnionDiscriminator("type")
]


class BetaManagedAgentsUserDefineOutcomeEvent(BaseModel):
    """Echo of a `user.define_outcome` input event.

    Carries the server-generated `outcome_id` that subsequent `span.outcome_evaluation_*` events reference.
    """

    id: str
    """Unique identifier for this event."""

    description: str
    """What the agent should produce. Copied from the input event."""

    max_iterations: Optional[int] = None
    """Evaluate-then-revise cycles before giving up. Default 3, max 20."""

    outcome_id: str
    """Server-generated `outc_` ID for this outcome.

    Referenced by `span.outcome_evaluation_*` events and the session's
    `outcome_evaluations` list.
    """

    processed_at: datetime
    """Timestamp when the outcome was accepted."""

    rubric: Rubric
    """How to grade the outcome.

    File rubrics are currently resolved to their text content; clients should handle
    both variants.
    """

    type: Literal["user.define_outcome"]
