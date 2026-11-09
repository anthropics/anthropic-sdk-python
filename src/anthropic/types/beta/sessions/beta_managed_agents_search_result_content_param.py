from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsSearchResultContentParam"]


class BetaManagedAgentsSearchResultContentParam(TypedDict, total=False):
    """Text content within a search result."""

    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
