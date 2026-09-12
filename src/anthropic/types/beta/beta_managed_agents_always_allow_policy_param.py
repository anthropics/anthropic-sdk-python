from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsAlwaysAllowPolicyParam"]


class BetaManagedAgentsAlwaysAllowPolicyParam(TypedDict, total=False):
    """Tool calls are automatically approved without user confirmation."""

    type: Required[Literal["always_allow"]]
