from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsWebFetchURLSourceAllParam"]


class BetaManagedAgentsWebFetchURLSourceAllParam(TypedDict, total=False):
    """Every URL from this source may be fetched. This is the default."""

    type: Required[Literal["all"]]
