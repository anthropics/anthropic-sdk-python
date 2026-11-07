from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Literal, Required, TypedDict

from .beta_mcp_tool_param_param import BetaMCPToolParamParam
from .beta_mcp_tool_config_param import BetaMCPToolConfigParam
from .beta_cache_control_ephemeral_param import BetaCacheControlEphemeralParam
from .beta_mcp_tool_default_config_param import BetaMCPToolDefaultConfigParam

__all__ = ["BetaMCPToolsetParam"]


class BetaMCPToolsetParam(TypedDict, total=False):
    """Configuration for a group of tools from an MCP server.

    Allows configuring enabled status and defer_loading for all tools
    from an MCP server, with optional per-tool overrides.
    """

    mcp_server_name: Required[str]
    """Name of the MCP server to configure tools for"""

    type: Required[Literal["mcp_toolset"]]

    cache_control: Optional[BetaCacheControlEphemeralParam]
    """Create a cache control breakpoint at this content block."""

    configs: Optional[Dict[str, BetaMCPToolConfigParam]]
    """Configuration overrides for specific tools, keyed by tool name"""

    default_config: BetaMCPToolDefaultConfigParam
    """Default configuration applied to all tools from this server"""

    tools: Optional[Iterable[BetaMCPToolParamParam]]
    """
    The server's tool listing, pinned: when present, the server is not asked for its
    tools before sampling and exactly these entries, with `default_config` and
    `configs` applied, are the toolset's tools. Copy it from the `mcp_tool_listing`
    block of an earlier response.
    """
