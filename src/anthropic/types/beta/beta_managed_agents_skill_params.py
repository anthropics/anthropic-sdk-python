from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_custom_skill_params import BetaManagedAgentsCustomSkillParams
from .beta_managed_agents_anthropic_skill_params import BetaManagedAgentsAnthropicSkillParams

__all__ = ["BetaManagedAgentsSkillParams"]

BetaManagedAgentsSkillParams: TypeAlias = Union[
    BetaManagedAgentsAnthropicSkillParams, BetaManagedAgentsCustomSkillParams
]
