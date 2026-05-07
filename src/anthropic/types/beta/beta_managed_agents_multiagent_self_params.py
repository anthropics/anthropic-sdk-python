# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsMultiagentSelfParams"]


class BetaManagedAgentsMultiagentSelfParams(TypedDict, total=False):
    """Sentinel roster entry meaning "the agent that owns this configuration".

    Resolved server-side to a concrete agent reference.
    """

    type: Required[Literal["self"]]
