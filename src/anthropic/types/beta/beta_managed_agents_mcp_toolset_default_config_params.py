from __future__ import annotations

from typing import Union, Optional
from typing_extensions import TypeAlias, TypedDict

from .beta_managed_agents_auto_policy_param import BetaManagedAgentsAutoPolicyParam
from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsMCPToolsetDefaultConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[
    BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam, BetaManagedAgentsAutoPolicyParam
]


class BetaManagedAgentsMCPToolsetDefaultConfigParams(TypedDict, total=False):
    """Default configuration for all tools from an MCP server."""

    enabled: Optional[bool]
    """Whether tools are enabled by default. Defaults to true if not specified."""

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""
