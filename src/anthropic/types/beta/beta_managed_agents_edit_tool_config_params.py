# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsEditToolConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam]


class BetaManagedAgentsEditToolConfigParams(TypedDict, total=False):
    """Configuration override for the edit tool."""

    name: Required[Literal["edit"]]
    """Must be "edit"."""

    enabled: Optional[bool]
    """Whether this tool is enabled and available to Claude.

    Overrides the default_config setting.
    """

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""

    type: Literal["edit"]
