from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..._types import SequenceNotStr
from .beta_managed_agents_auto_policy_param import BetaManagedAgentsAutoPolicyParam
from .beta_managed_agents_always_ask_policy_param import BetaManagedAgentsAlwaysAskPolicyParam
from .beta_managed_agents_always_allow_policy_param import BetaManagedAgentsAlwaysAllowPolicyParam

__all__ = ["BetaManagedAgentsWebFetchToolConfigParams", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Union[
    BetaManagedAgentsAlwaysAllowPolicyParam, BetaManagedAgentsAlwaysAskPolicyParam, BetaManagedAgentsAutoPolicyParam
]


class BetaManagedAgentsWebFetchToolConfigParams(TypedDict, total=False):
    """Configuration override for the web_fetch tool."""

    name: Required[Literal["web_fetch"]]
    """Must be "web_fetch"."""

    allowed_domains: SequenceNotStr[str]
    """Only fetch URLs whose host is one of these domains or a subdomain of one.

    Each entry is a plain hostname like "docs.example.com" (no scheme, port, or
    path). At most 64 entries; an empty list is rejected (omit the field instead).
    Cannot be combined with blocked_domains.
    """

    blocked_domains: SequenceNotStr[str]
    """Never fetch URLs whose host is one of these domains or a subdomain of one.

    Each entry is a plain hostname like "ads.example.com" (no scheme, port, or
    path). At most 64 entries; an empty list is rejected (omit the field instead).
    Cannot be combined with allowed_domains.
    """

    enabled: Optional[bool]
    """Whether this tool is enabled and available to Claude.

    Overrides the default_config setting.
    """

    max_content_tokens: Optional[int]
    """Maximum number of tokens of fetched text content to include in context per call.

    Does not apply to binary content such as PDFs.
    """

    permission_policy: Optional[PermissionPolicy]
    """Permission policy for tool execution."""

    type: Literal["web_fetch"]
