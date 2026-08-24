# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsReadToolConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam]


class BetaManagedAgentsReadToolConfigParams(TypedDict, total=False):
    """Configuration override for the read tool."""

    name: Required[Literal["read"]]
    """Must be "read"."""

    enabled: Optional[bool]
    """Whether this tool is enabled and available to Claude.

    Overrides the default_config setting.
    """

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""

    type: Literal["read"]
