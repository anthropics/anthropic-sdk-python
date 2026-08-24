# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_always_ask_policy import BetaManagedAgentsAlwaysAskPolicy
from .beta_managed_agents_always_allow_policy import BetaManagedAgentsAlwaysAllowPolicy

__all__ = ["BetaManagedAgentsWebFetchToolConfig", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Annotated[
    Union[BetaManagedAgentsAlwaysAllowPolicy, BetaManagedAgentsAlwaysAskPolicy], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsWebFetchToolConfig(BaseModel):
    """Configuration for the web_fetch tool."""

    enabled: bool

    name: Literal["web_fetch"]

    permission_policy: PermissionPolicy
    """Permission policy for tool execution."""

    type: Literal["web_fetch"]

    allowed_domains: Optional[List[str]] = None

    blocked_domains: Optional[List[str]] = None

    max_content_tokens: Optional[int] = None
