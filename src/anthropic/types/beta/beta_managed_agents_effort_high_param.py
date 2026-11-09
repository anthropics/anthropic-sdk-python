from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsEffortHighParam"]


class BetaManagedAgentsEffortHighParam(TypedDict, total=False):
    """High effort. Favors reasoning depth."""

    type: Required[Literal["high"]]
