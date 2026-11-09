from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_session_thread_agent import BetaManagedAgentsSessionThreadAgent
from .beta_managed_agents_multiagent_inline_agents import BetaManagedAgentsMultiagentInlineAgents

__all__ = ["BetaManagedAgentsSessionMultiagentWorkflowsEnabled"]


class BetaManagedAgentsSessionMultiagentWorkflowsEnabled(BaseModel):
    """The agent can start workflow runs."""

    inline_agents: BetaManagedAgentsMultiagentInlineAgents
    """Whether a run's plan can define inline agents, which are not saved."""

    predefined_agents: List[BetaManagedAgentsSessionThreadAgent]
    """
    Full `agent` definitions of the predefined agents, which are saved agents that a
    run's plan can use.
    """

    type: Literal["enabled"]
