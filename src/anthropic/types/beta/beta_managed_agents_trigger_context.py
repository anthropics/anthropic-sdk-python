# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_manual_trigger_context import BetaManagedAgentsManualTriggerContext
from .beta_managed_agents_schedule_trigger_context import BetaManagedAgentsScheduleTriggerContext

__all__ = ["BetaManagedAgentsTriggerContext"]

BetaManagedAgentsTriggerContext: TypeAlias = Annotated[
    Union[BetaManagedAgentsScheduleTriggerContext, BetaManagedAgentsManualTriggerContext],
    PropertyInfo(discriminator="type"),
]
