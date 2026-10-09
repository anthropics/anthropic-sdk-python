from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_multiagent_advisor import BetaManagedAgentsMultiagentAdvisor
from .beta_managed_agents_session_multiagent_subagents import BetaManagedAgentsSessionMultiagentSubagents
from .beta_managed_agents_session_multiagent_workflows import BetaManagedAgentsSessionMultiagentWorkflows

__all__ = ["BetaManagedAgentsSessionMultiagent20261001"]


class BetaManagedAgentsSessionMultiagent20261001(BaseModel):
    """
    Resolved multiagent configuration with three members, as copied to the `session` at creation.
    """

    advisor: BetaManagedAgentsMultiagentAdvisor
    """Whether the session's primary thread can consult an advisor model."""

    subagents: BetaManagedAgentsSessionMultiagentSubagents
    """Whether the agent can spawn session threads."""

    type: Literal["multiagent_20261001"]

    workflows: BetaManagedAgentsSessionMultiagentWorkflows
    """Whether the agent can start workflow runs."""
