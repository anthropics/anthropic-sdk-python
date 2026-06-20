# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .sessions.beta_managed_agents_file_rubric import BetaManagedAgentsFileRubric
from .sessions.beta_managed_agents_text_rubric import BetaManagedAgentsTextRubric

__all__ = ["BetaManagedAgentsDeploymentUserDefineOutcomeEvent", "Rubric"]

Rubric: TypeAlias = Annotated[
    Union[BetaManagedAgentsFileRubric, BetaManagedAgentsTextRubric], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsDeploymentUserDefineOutcomeEvent(BaseModel):
    """An outcome the agent should work toward. The agent begins work on receipt."""

    description: str
    """What the agent should produce. This is the task specification."""

    rubric: Rubric
    """Rubric for grading the quality of an outcome."""

    type: Literal["user.define_outcome"]

    max_iterations: Optional[int] = None
    """Eval→revision cycles before giving up. Default 3, max 20."""
