from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsWebFetchURLSourceNoneParam"]


class BetaManagedAgentsWebFetchURLSourceNoneParam(TypedDict, total=False):
    """This source contributes no URLs that may be fetched."""

    type: Required[Literal["none"]]
