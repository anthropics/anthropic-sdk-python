# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .beta_managed_agents_agent_message_preview import BetaManagedAgentsAgentMessagePreview
from .beta_managed_agents_agent_thinking_preview import BetaManagedAgentsAgentThinkingPreview

__all__ = ["BetaManagedAgentsStartEventPreview"]

BetaManagedAgentsStartEventPreview: TypeAlias = Annotated[
    Union[BetaManagedAgentsAgentMessagePreview, BetaManagedAgentsAgentThinkingPreview],
    PropertyInfo(discriminator="type"),
]
