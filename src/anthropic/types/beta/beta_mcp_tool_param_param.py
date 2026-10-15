from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["BetaMCPToolParamParam"]


class BetaMCPToolParamParam(TypedDict, total=False):
    """
    A tool as an MCP server lists it: its name on that server, its
    description, and its input schema.
    """

    input_schema: Required[Dict[str, object]]
    """The tool's input schema as the MCP server lists it, verbatim."""

    name: Required[str]
    """The tool's name as the MCP server lists it (not prefixed with the server name)."""

    description: Optional[str]
    """The tool's description as the MCP server lists it."""
