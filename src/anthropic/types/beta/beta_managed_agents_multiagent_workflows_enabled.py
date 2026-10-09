from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference
from .beta_managed_agents_multiagent_inline_agents import BetaManagedAgentsMultiagentInlineAgents

__all__ = ["BetaManagedAgentsMultiagentWorkflowsEnabled"]


class BetaManagedAgentsMultiagentWorkflowsEnabled(BaseModel):
    """The agent can start workflow runs."""

    inline_agents: BetaManagedAgentsMultiagentInlineAgents
    """Whether a run's plan can define inline agents, which are not saved."""

    predefined_agents: List[BetaManagedAgentsAgentReference]
    """
    Predefined agents, which are saved agents that a run's plan can use, each
    resolved to a specific version.
    """

    type: Literal["enabled"]
