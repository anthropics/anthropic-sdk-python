# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .beta_managed_agents_agent_reference import BetaManagedAgentsAgentReference

__all__ = ["BetaManagedAgentsMultiagent"]


class BetaManagedAgentsMultiagent(BaseModel):
    """Resolved coordinator topology with a concrete agent roster."""

    agents: List[BetaManagedAgentsAgentReference]
    """
    Agents the coordinator may spawn as session threads, each resolved to a specific
    version.
    """

    type: Literal["coordinator"]
