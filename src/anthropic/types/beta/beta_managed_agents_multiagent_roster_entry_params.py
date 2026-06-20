# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_agent_params import BetaManagedAgentsAgentParams
from .beta_managed_agents_multiagent_self_params import BetaManagedAgentsMultiagentSelfParams

__all__ = ["BetaManagedAgentsMultiagentRosterEntryParams"]

BetaManagedAgentsMultiagentRosterEntryParams: TypeAlias = Union[
    str, BetaManagedAgentsAgentParams, BetaManagedAgentsMultiagentSelfParams
]
