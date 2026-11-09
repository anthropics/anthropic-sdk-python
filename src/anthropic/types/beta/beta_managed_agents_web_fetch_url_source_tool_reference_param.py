from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsWebFetchURLSourceToolReferenceParam"]


class BetaManagedAgentsWebFetchURLSourceToolReferenceParam(TypedDict, total=False):
    """Names one tool in an only or except list."""

    name: Required[str]
    """Name of the tool.

    Compared exactly, so upper and lower case letters are different.
    """

    type: Required[Literal["tool_reference"]]
    """Must be "tool_reference"."""
