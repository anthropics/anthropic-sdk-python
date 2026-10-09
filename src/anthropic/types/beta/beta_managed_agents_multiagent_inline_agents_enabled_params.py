from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentInlineAgentsEnabledParams"]


class BetaManagedAgentsMultiagentInlineAgentsEnabledParams(TypedDict, total=False):
    """The agent can define inline agents."""

    type: Required[Literal["enabled"]]
