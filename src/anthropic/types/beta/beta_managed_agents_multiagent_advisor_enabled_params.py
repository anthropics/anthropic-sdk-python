from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentAdvisorEnabledParams"]


class BetaManagedAgentsMultiagentAdvisorEnabledParams(TypedDict, total=False):
    """The session's primary thread can consult `model` mid-turn."""

    model: Required[str]
    """A Claude model id.

    The model must be permitted as an advisor for this agent's model.
    """

    type: Required[Literal["enabled"]]
