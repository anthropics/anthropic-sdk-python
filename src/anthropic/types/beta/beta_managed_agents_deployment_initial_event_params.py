# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

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
