from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsEffortMaxParam"]


class BetaManagedAgentsEffortMaxParam(TypedDict, total=False):
    """Maximum effort. Favors reasoning depth over latency."""

    type: Required[Literal["max"]]
