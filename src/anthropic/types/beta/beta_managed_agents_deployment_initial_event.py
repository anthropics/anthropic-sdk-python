# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_deployment_user_message_event import BetaManagedAgentsDeploymentUserMessageEvent
from .beta_managed_agents_deployment_system_message_event import BetaManagedAgentsDeploymentSystemMessageEvent
from .beta_managed_agents_deployment_user_define_outcome_event import BetaManagedAgentsDeploymentUserDefineOutcomeEvent

__all__ = ["BetaManagedAgentsDeploymentInitialEvent"]

BetaManagedAgentsDeploymentInitialEvent: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsDeploymentUserMessageEvent,
        BetaManagedAgentsDeploymentUserDefineOutcomeEvent,
        BetaManagedAgentsDeploymentSystemMessageEvent,
    ],
    PropertyInfo(discriminator="type"),
]
