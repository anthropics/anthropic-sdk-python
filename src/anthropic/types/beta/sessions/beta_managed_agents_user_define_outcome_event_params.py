# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_file_rubric_params import BetaManagedAgentsFileRubricParams
from .beta_managed_agents_text_rubric_params import BetaManagedAgentsTextRubricParams

__all__ = ["BetaManagedAgentsUserDefineOutcomeEventParams", "Rubric"]

Rubric: TypeAlias = Union[BetaManagedAgentsFileRubricParams, BetaManagedAgentsTextRubricParams]


class BetaManagedAgentsUserDefineOutcomeEventParams(TypedDict, total=False):
    """Parameters for defining an outcome the agent should work toward.

    The agent begins work on receipt.
    """

    description: Required[str]
    """What the agent should produce. This is the task specification."""

    rubric: Required[Rubric]
    """Rubric for grading the quality of an outcome."""

    type: Required[Literal["user.define_outcome"]]

    max_iterations: Optional[int]
    """Eval→revision cycles before giving up. Default 3, max 20."""
