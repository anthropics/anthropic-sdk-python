from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentWorkflowsDisabledParams"]


class BetaManagedAgentsMultiagentWorkflowsDisabledParams(TypedDict, total=False):
    """The agent cannot start workflow runs."""

    type: Required[Literal["disabled"]]
