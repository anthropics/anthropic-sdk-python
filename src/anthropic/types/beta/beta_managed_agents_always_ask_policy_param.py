from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsAlwaysAskPolicyParam"]


class BetaManagedAgentsAlwaysAskPolicyParam(TypedDict, total=False):
    """Tool calls require user confirmation before execution."""

    type: Required[Literal["always_ask"]]
