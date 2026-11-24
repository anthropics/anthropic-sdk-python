from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .sessions.beta_managed_agents_user_message_event_params import BetaManagedAgentsUserMessageEventParams
from .sessions.beta_managed_agents_system_message_event_params import BetaManagedAgentsSystemMessageEventParams
from .sessions.beta_managed_agents_user_define_outcome_event_params import BetaManagedAgentsUserDefineOutcomeEventParams

__all__ = ["BetaManagedAgentsDeploymentInitialEventParams"]

BetaManagedAgentsDeploymentInitialEventParams: TypeAlias = Union[
    BetaManagedAgentsUserMessageEventParams,
    BetaManagedAgentsUserDefineOutcomeEventParams,
    BetaManagedAgentsSystemMessageEventParams,
]
"""An event sent to a session immediately after it is created.

Supports `user.message`, `user.define_outcome`, and `system.message`.
"""
