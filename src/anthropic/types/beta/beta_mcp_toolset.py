from typing import Dict, List, Optional
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_mcp_tool_param import BetaMCPToolParam
from .beta_mcp_tool_config import BetaMCPToolConfig
from .beta_cache_control_ephemeral import BetaCacheControlEphemeral
from .beta_mcp_tool_default_config import BetaMCPToolDefaultConfig

__all__ = ["BetaMCPToolset"]


class BetaMCPToolset(BaseModel):
    """Configuration for a group of tools from an MCP server.

    Allows configuring enabled status and defer_loading for all tools
    from an MCP server, with optional per-tool overrides.
    """

    mcp_server_name: str
    """Name of the MCP server to configure tools for"""

    type: Literal["mcp_toolset"]

    cache_control: Optional[BetaCacheControlEphemeral] = None
    """Create a cache control breakpoint at this content block."""

    configs: Optional[Dict[str, BetaMCPToolConfig]] = None
    """Configuration overrides for specific tools, keyed by tool name"""

    default_config: Optional[BetaMCPToolDefaultConfig] = None
    """Default configuration applied to all tools from this server"""

    tools: Optional[List[BetaMCPToolParam]] = None
    """
    The server's tool listing, pinned: when present, the server is not asked for its
    tools before sampling and exactly these entries, with `default_config` and
    `configs` applied, are the toolset's tools. Copy it from the `mcp_tool_listing`
    block of an earlier response.
    """
