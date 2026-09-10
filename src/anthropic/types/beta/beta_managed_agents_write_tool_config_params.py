from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_auto_policy_param import BetaManagedAgentsAutoPolicyParam
from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsWriteToolConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[
    BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam, BetaManagedAgentsAutoPolicyParam
]


class BetaManagedAgentsWriteToolConfigParams(TypedDict, total=False):
    """Configuration override for the write tool."""

    name: Required[Literal["write"]]
    """Must be "write"."""

    enabled: Optional[bool]
    """Whether this tool is enabled and available to Claude.

    Overrides the default_config setting.
    """

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""

    type: Literal["write"]
