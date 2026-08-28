# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._models import BaseModel, UnionDiscriminator
from .beta_managed_agents_always_ask_policy import BetaManagedAgentsAlwaysAskPolicy
from .beta_managed_agents_always_allow_policy import BetaManagedAgentsAlwaysAllowPolicy

__all__ = ["BetaManagedAgentsGrepToolConfig", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Annotated[
    Union[BetaManagedAgentsAlwaysAllowPolicy, BetaManagedAgentsAlwaysAskPolicy], UnionDiscriminator("type")
]


class BetaManagedAgentsGrepToolConfig(BaseModel):
    """Configuration for the grep tool."""

    enabled: bool

    name: Literal["grep"]

    permission_policy: PermissionPolicy
    """Permission policy for tool execution."""

    type: Literal["grep"]
