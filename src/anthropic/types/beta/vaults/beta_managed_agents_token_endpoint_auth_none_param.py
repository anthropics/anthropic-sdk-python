from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsTokenEndpointAuthNoneParam"]


class BetaManagedAgentsTokenEndpointAuthNoneParam(TypedDict, total=False):
    """Token endpoint requires no client authentication."""

    type: Required[Literal["none"]]
