# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import Literal, Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_managed_agents_advisor import BetaManagedAgentsAdvisor
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference

__all__ = ["BetaManagedAgentsMultiagent", "Agent"]

Agent: TypeAlias = Annotated[
    Union[BetaManagedAgentsAgentReference, BetaManagedAgentsAdvisor], PropertyInfo(discriminator="type")
]


class BetaManagedAgentsMultiagent(BaseModel):
    """Resolved coordinator topology with a concrete agent roster."""

    agents: List[Agent]
    """
    Agents the coordinator may spawn as session threads, each resolved to a specific
    version.
    """

    type: Literal["coordinator"]
