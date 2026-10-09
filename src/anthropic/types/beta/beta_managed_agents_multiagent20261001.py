from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_multiagent_advisor import BetaManagedAgentsMultiagentAdvisor
from .beta_managed_agents_multiagent_subagents import BetaManagedAgentsMultiagentSubagents
from .beta_managed_agents_multiagent_workflows import BetaManagedAgentsMultiagentWorkflows

__all__ = ["BetaManagedAgentsMultiagent20261001"]


class BetaManagedAgentsMultiagent20261001(BaseModel):
    """
    Resolved multiagent configuration with three members, each enabled or disabled on its own.
    """

    advisor: BetaManagedAgentsMultiagentAdvisor
    """Whether the session's primary thread can consult an advisor model."""

    subagents: BetaManagedAgentsMultiagentSubagents
    """Whether the agent can spawn session threads."""

    type: Literal["multiagent_20261001"]

    workflows: BetaManagedAgentsMultiagentWorkflows
    """Whether the agent can start workflow runs."""
