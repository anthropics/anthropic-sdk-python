from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentAdvisorDisabledParams"]


class BetaManagedAgentsMultiagentAdvisorDisabledParams(TypedDict, total=False):
    """The agent has no advisor."""

    type: Required[Literal["disabled"]]
