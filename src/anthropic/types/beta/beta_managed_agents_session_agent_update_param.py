# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import TypeAlias, TypedDict

from .beta_managed_agents_custom_tool_params import BetaManagedAgentsCustomToolParams
from .beta_managed_agents_mcp_toolset_params import BetaManagedAgentsMCPToolsetParams
from .beta_managed_agents_url_mcp_server_params import BetaManagedAgentsURLMCPServerParams
from .beta_managed_agents_agent_toolset20260401_params import BetaManagedAgentsAgentToolset20260401Params

__all__ = ["BetaManagedAgentsSessionAgentUpdateParam", "Tool"]

Tool: TypeAlias = Union[
    BetaManagedAgentsAgentToolset20260401Params, BetaManagedAgentsMCPToolsetParams, BetaManagedAgentsCustomToolParams
]


class BetaManagedAgentsSessionAgentUpdateParam(TypedDict, total=False):
    """Mid-session agent configuration update.

    Only `tools` and `mcp_servers` are updatable. Full replacement: the provided array becomes the new value. To preserve existing entries, GET the session, modify the array, and POST it back.
    """

    mcp_servers: Iterable[BetaManagedAgentsURLMCPServerParams]
    """Replacement MCP server list.

    Full replacement: the provided array becomes the new value. Send an empty array
    to clear; omit to preserve.
    """

    tools: Iterable[Tool]
    """Replacement tool list.

    Full replacement: the provided array becomes the new value. Send an empty array
    to clear; omit to preserve.
    """
