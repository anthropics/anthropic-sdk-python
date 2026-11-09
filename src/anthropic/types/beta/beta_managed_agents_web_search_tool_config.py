from typing import List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_auto_policy import BetaManagedAgentsAutoPolicy
from .beta_managed_agents_user_location import BetaManagedAgentsUserLocation
from .beta_managed_agents_always_ask_policy import BetaManagedAgentsAlwaysAskPolicy
from .beta_managed_agents_always_allow_policy import BetaManagedAgentsAlwaysAllowPolicy

__all__ = ["BetaManagedAgentsWebSearchToolConfig", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Annotated[
    Union[BetaManagedAgentsAlwaysAllowPolicy, BetaManagedAgentsAlwaysAskPolicy, BetaManagedAgentsAutoPolicy],
    UnionDiscriminator("type"),
]


class BetaManagedAgentsWebSearchToolConfig(BaseModel):
    """Configuration for the web_search tool."""

    enabled: bool

    name: Literal["web_search"]

    permission_policy: PermissionPolicy
    """Permission policy for tool execution."""

    type: Literal["web_search"]

    allowed_domains: Optional[List[str]] = None

    blocked_domains: Optional[List[str]] = None

    user_location: Optional[BetaManagedAgentsUserLocation] = None
    """Approximate user location for search result localization."""
