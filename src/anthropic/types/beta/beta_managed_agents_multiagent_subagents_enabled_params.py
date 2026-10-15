from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr
from .beta_managed_agents_multiagent_inline_agents_params import BetaManagedAgentsMultiagentInlineAgentsParams
from .beta_managed_agents_multiagent_predefined_agent_params import BetaManagedAgentsMultiagentPredefinedAgentParams

__all__ = ["BetaManagedAgentsMultiagentSubagentsEnabledParams"]


class BetaManagedAgentsMultiagentSubagentsEnabledParams(TypedDict, total=False):
    """The agent can spawn session threads.

    Each thread runs a predefined agent, which is a saved agent in `predefined_agents`, or an inline agent, which the agent defines when it spawns the thread and which is not saved. If `inline_agents` is disabled, `predefined_agents` must name at least one agent.
    """

    type: Required[Literal["enabled"]]

    inline_agents: Optional[BetaManagedAgentsMultiagentInlineAgentsParams]
    """Whether the agent can define inline agents when it spawns session threads.

    Defaults to enabled.
    """

    predefined_agents: Optional[SequenceNotStr[BetaManagedAgentsMultiagentPredefinedAgentParams]]
    """Predefined agents that this agent can spawn as session threads.

    At most 20. Defaults to null. Null and an empty list both mean no predefined
    agents. This list is separate from `workflows.predefined_agents`, and an agent
    in one list is not added to the other.
    """
