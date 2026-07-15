# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_model_param import BetaManagedAgentsModelParam
from .beta_managed_agents_skill_params import BetaManagedAgentsSkillParams
from .beta_managed_agents_custom_tool_params import BetaManagedAgentsCustomToolParams
from .beta_managed_agents_mcp_toolset_params import BetaManagedAgentsMCPToolsetParams
from .beta_managed_agents_model_config_params import BetaManagedAgentsModelConfigParams
from .beta_managed_agents_url_mcp_server_params import BetaManagedAgentsURLMCPServerParams
from .beta_managed_agents_agent_toolset20260401_params import BetaManagedAgentsAgentToolset20260401Params

__all__ = ["BetaManagedAgentsAgentWithOverridesParams", "Model", "Tool"]

Model: TypeAlias = Union[BetaManagedAgentsModelParam, BetaManagedAgentsModelConfigParams]

Tool: TypeAlias = Union[
    BetaManagedAgentsAgentToolset20260401Params, BetaManagedAgentsMCPToolsetParams, BetaManagedAgentsCustomToolParams
]


class BetaManagedAgentsAgentWithOverridesParams(TypedDict, total=False):
    """Reference to an `agent` plus optional configuration overrides.

    Each provided field replaces the agent's value for the caller's use; the agent resource is unchanged.
    """

    id: Required[str]
    """The `agent` ID."""

    type: Required[Literal["agent_with_overrides"]]

    mcp_servers: Iterable[BetaManagedAgentsURLMCPServerParams]
    """Replacement MCP server list.

    Full replacement: the provided array becomes the MCP servers. Send an empty
    array to clear; omit to preserve the agent's servers.
    """

    model: Model
    """Replacement model.

    Accepts the model string, e.g. `claude-opus-4-6`, or a `model_config` object.
    Omit to use the agent's model.
    """

    skills: Iterable[BetaManagedAgentsSkillParams]
    """Replacement skill list.

    Full replacement: the provided array becomes the skills. Send an empty array to
    clear; omit to preserve the agent's skills.
    """

    system: Optional[str]
    """Replacement system prompt.

    Up to 100,000 characters. Set to null to clear the agent's system prompt; omit
    to preserve it.
    """

    tools: Iterable[Tool]
    """Replacement tool list.

    Full replacement: the provided array becomes the tool configuration. Send an
    empty array to clear; omit to preserve the agent's tools.
    """

    version: int
    """The specific `agent` version to use. Omit to use the latest version."""
