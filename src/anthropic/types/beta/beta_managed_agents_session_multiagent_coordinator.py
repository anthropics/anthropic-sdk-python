# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ..._models import BaseModel
from .sessions.beta_managed_agents_session_thread_agent import BetaManagedAgentsSessionThreadAgent

__all__ = ["BetaManagedAgentsSessionMultiagentCoordinator"]


class BetaManagedAgentsSessionMultiagentCoordinator(BaseModel):
    """
    Resolved coordinator topology with full agent definitions for each roster member.
    """

    agents: List[BetaManagedAgentsSessionThreadAgent]
    """Full `agent` definitions the coordinator may spawn as session threads."""

    type: Literal["coordinator"]
