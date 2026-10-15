from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_auto_policy import BetaManagedAgentsAutoPolicy
from .beta_managed_agents_always_ask_policy import BetaManagedAgentsAlwaysAskPolicy
from .beta_managed_agents_always_allow_policy import BetaManagedAgentsAlwaysAllowPolicy
from .beta_managed_agents_web_fetch_url_sources import BetaManagedAgentsWebFetchURLSources

__all__ = ["BetaManagedAgentsWebFetchToolConfig", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Annotated[
    Union[BetaManagedAgentsAlwaysAllowPolicy, BetaManagedAgentsAlwaysAskPolicy, BetaManagedAgentsAutoPolicy],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsWebFetchToolConfig(BaseModel):
    """Configuration for the web_fetch tool."""

    enabled: bool

    name: Literal["web_fetch"]

    permission_policy: PermissionPolicy
    """Permission policy for tool execution."""

    type: Literal["web_fetch"]

    url_sources: Optional[BetaManagedAgentsWebFetchURLSources] = None
    """Which sources contribute URLs the tool may fetch, always in the object form.

    Null when not set, which allows every source.
    """

    allowed_domains: Optional[List[str]] = None

    blocked_domains: Optional[List[str]] = None

    max_content_tokens: Optional[int] = None
