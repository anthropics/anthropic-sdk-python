from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginComponent"]


class BetaPluginComponent(BaseModel):
    description: Optional[str] = None
    """
    What the component declares about itself; always null for MCP servers, hooks,
    and CLIs.
    """

    name: str
    """
    The component's name: a skill's, command's or agent's name, an MCP server's key
    in the manifest, the event a hook runs on, or a CLI's executable.
    """

    type: Literal["agent", "cli", "command", "hook", "mcp_server", "skill"]
    """The kind of component."""
