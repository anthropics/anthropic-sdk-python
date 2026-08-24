# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from .beta_managed_agents_user_location_param import BetaManagedAgentsUserLocationParam
from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsWebSearchToolConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam]


class BetaManagedAgentsWebSearchToolConfigParams(TypedDict, total=False):
    """Configuration override for the web_search tool."""

    name: Required[Literal["web_search"]]
    """Must be "web_search"."""

    allowed_domains: SequenceNotStr[str]
    """
    Only return search results whose host is one of these domains or a subdomain of
    one. Each entry is a plain hostname like "docs.example.com" (no scheme or port;
    an optional path suffix is accepted). At most 64 entries; an empty list is
    rejected (omit the field instead). Cannot be combined with blocked_domains.
    """

    blocked_domains: SequenceNotStr[str]
    """
    Never return search results whose host is one of these domains or a subdomain of
    one. Each entry is a plain hostname like "ads.example.com" (no scheme or port;
    an optional path suffix is accepted). At most 64 entries; an empty list is
    rejected (omit the field instead). Cannot be combined with allowed_domains.
    """

    enabled: Optional[bool]
    """Whether this tool is enabled and available to Claude.

    Overrides the default_config setting.
    """

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""

    type: Literal["web_search"]

    user_location: Optional[BetaManagedAgentsUserLocationParam]
    """Approximate user location for search result localization."""
