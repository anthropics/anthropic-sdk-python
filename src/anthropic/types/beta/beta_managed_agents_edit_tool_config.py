# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_always_ask_policy import BetaManagedAgentsAlwaysAskPolicy
from .beta_managed_agents_always_allow_policy import BetaManagedAgentsAlwaysAllowPolicy

__all__ = ["BetaManagedAgentsEditToolConfig", "PermissionPolicy"]

PermissionPolicy: TypeAlias = Annotated[
    Union[BetaManagedAgentsAlwaysAllowPolicy, BetaManagedAgentsAlwaysAskPolicy], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsEditToolConfig(BaseModel):
    """Configuration for the edit tool."""

    enabled: bool

    name: Literal["edit"]

    permission_policy: PermissionPolicy
    """Permission policy for tool execution."""

    type: Literal["edit"]
