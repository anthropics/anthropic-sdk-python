from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsTextBlockParam"]


class BetaManagedAgentsTextBlockParam(TypedDict, total=False):
    """Regular text content."""

    text: Required[str]
    """The text content."""

    type: Required[Literal["text"]]
