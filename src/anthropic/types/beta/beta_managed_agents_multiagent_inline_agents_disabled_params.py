from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentInlineAgentsDisabledParams"]


class BetaManagedAgentsMultiagentInlineAgentsDisabledParams(TypedDict, total=False):
    """The agent cannot define inline agents."""

    type: Required[Literal["disabled"]]
