# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_advisor import BetaManagedAgentsAdvisor
from .beta_managed_agents_session_thread_agent import BetaManagedAgentsSessionThreadAgent

__all__ = ["BetaManagedAgentsSessionMultiagentCoordinator", "Agent"]

Agent: TypeAlias = Annotated[
    Union[BetaManagedAgentsSessionThreadAgent, BetaManagedAgentsAdvisor], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsSessionMultiagentCoordinator(BaseModel):
    """
    Resolved coordinator topology with full agent definitions for each roster member.
    """

    agents: List[Agent]
    """Full `agent` definitions the coordinator may spawn as session threads."""

    type: Literal["coordinator"]
