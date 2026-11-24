from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_agent_params import BetaManagedAgentsAgentParams
from .beta_managed_agents_multiagent_self_params import BetaManagedAgentsMultiagentSelfParams

__all__ = ["BetaManagedAgentsMultiagentPredefinedAgentParams"]

BetaManagedAgentsMultiagentPredefinedAgentParams: TypeAlias = Union[
    str, BetaManagedAgentsAgentParams, BetaManagedAgentsMultiagentSelfParams
]
"""One agent in a `predefined_agents` list.

It is an agent ID string, an `agent` reference with an optional `version`, or `self` for the agent that owns this configuration.
"""
