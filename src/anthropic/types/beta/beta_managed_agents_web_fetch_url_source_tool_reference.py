from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsWebFetchURLSourceToolReference"]


class BetaManagedAgentsWebFetchURLSourceToolReference(BaseModel):
    """Names one tool in an only or except list."""

    name: str
    """Name of the tool.

    Compared exactly, so upper and lower case letters are different.
    """

    type: Literal["tool_reference"]
    """Must be "tool_reference"."""
