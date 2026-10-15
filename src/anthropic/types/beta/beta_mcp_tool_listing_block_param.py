from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .beta_mcp_tool_param_param import BetaMCPToolParamParam

__all__ = ["BetaMCPToolListingBlockParam"]


class BetaMCPToolListingBlockParam(TypedDict, total=False):
    """
    The tool listing an MCP server returned while an earlier response was
    produced, as that response carried it. Send the assistant message back
    unchanged, this block included, and the server uses this listing for the
    matching `mcp_toolset` instead of asking the MCP server again.
    """

    mcp_server_name: Required[str]
    """
    The name of the MCP server this listing came from, as `mcp_servers` declares it.
    """

    tools: Required[Iterable[BetaMCPToolParamParam]]
    """The server's tools, exactly as the response listed them."""

    type: Required[Literal["mcp_tool_listing"]]
