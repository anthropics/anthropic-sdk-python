from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from .beta_managed_agents_auto_policy_param import BetaManagedAgentsAutoPolicyParam
from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsMCPToolConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[
    BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam, BetaManagedAgentsAutoPolicyParam
]


class BetaManagedAgentsMCPToolConfigParams(TypedDict, total=False):
    """Configuration override for a specific MCP tool."""

    name: Required[str]
    """Name of the MCP tool to configure. 1-128 characters."""

    enabled: Optional[bool]
    """Whether this tool is enabled. Overrides the `default_config` setting."""

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""
