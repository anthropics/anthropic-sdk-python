from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from .beta_managed_agents_multiagent_inline_agents_params import BetaManagedAgentsMultiagentInlineAgentsParams
from .beta_managed_agents_multiagent_predefined_agent_params import BetaManagedAgentsMultiagentPredefinedAgentParams

__all__ = ["BetaManagedAgentsMultiagentWorkflowsEnabledParams"]


class BetaManagedAgentsMultiagentWorkflowsEnabledParams(TypedDict, total=False):
    """The agent can start workflow runs.

    Each run follows a plan, a program that the agent writes. A plan can use predefined agents, which are the saved agents in `predefined_agents`, and inline agents, which it defines itself and which are not saved. If `inline_agents` is disabled, `predefined_agents` must name at least one agent.
    """

    type: Required[Literal["enabled"]]

    inline_agents: Optional[BetaManagedAgentsMultiagentInlineAgentsParams]
    """Whether a run's plan can define inline agents. Defaults to enabled."""

    predefined_agents: Optional[SequenceNotStr[BetaManagedAgentsMultiagentPredefinedAgentParams]]
    """Predefined agents that a run's plan can use.

    At most 20. Defaults to null. Null and an empty list both mean no predefined
    agents. This list is separate from `subagents.predefined_agents`, and an agent
    in one list is not added to the other.
    """
