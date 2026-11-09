from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentSubagentsDisabledParams"]


class BetaManagedAgentsMultiagentSubagentsDisabledParams(TypedDict, total=False):
    """The agent cannot spawn session threads."""

    type: Required[Literal["disabled"]]
