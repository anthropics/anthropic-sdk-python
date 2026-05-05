# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_managed_agents_file_rubric import BetaManagedAgentsFileRubric
from .beta_managed_agents_text_rubric import BetaManagedAgentsTextRubric

__all__ = ["BetaManagedAgentsUserDefineOutcomeEvent", "Rubric"]

Rubric: TypeAlias = Annotated[
    Union[BetaManagedAgentsFileRubric, BetaManagedAgentsTextRubric], PropertyInfo(discriminator="type")
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
    """A timestamp in RFC 3339 format"""

    rubric: Rubric
    """Rubric for grading the quality of an outcome."""

    type: Literal["user.define_outcome"]
