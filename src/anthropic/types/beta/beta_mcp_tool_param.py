from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["BetaMCPToolParam"]


class BetaMCPToolParam(BaseModel):
    """
    A tool as an MCP server lists it: its name on that server, its
    description, and its input schema.
    """

    input_schema: Dict[str, object]
    """The tool's input schema as the MCP server lists it, verbatim."""

    name: str
    """The tool's name as the MCP server lists it (not prefixed with the server name)."""

    description: Optional[str] = None
    """The tool's description as the MCP server lists it."""
