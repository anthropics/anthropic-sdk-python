from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference
from .beta_managed_agents_multiagent_inline_agents import BetaManagedAgentsMultiagentInlineAgents

__all__ = ["BetaManagedAgentsMultiagentSubagentsEnabled"]


class BetaManagedAgentsMultiagentSubagentsEnabled(BaseModel):
    """The agent can spawn session threads."""

    inline_agents: BetaManagedAgentsMultiagentInlineAgents
    """
    Whether the agent can define inline agents, which are not saved, when it spawns
    session threads.
    """

    predefined_agents: List[BetaManagedAgentsAgentReference]
    """
    Predefined agents, which are saved agents that this agent can spawn as session
    threads, each resolved to a specific version.
    """

    type: Literal["enabled"]
