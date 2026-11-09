from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsURLImageSourceParam"]


class BetaManagedAgentsURLImageSourceParam(TypedDict, total=False):
    """Image referenced by URL."""

    type: Required[Literal["url"]]

    url: Required[str]
    """URL of the image to fetch."""
