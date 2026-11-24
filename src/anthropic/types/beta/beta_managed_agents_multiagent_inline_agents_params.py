from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_multiagent_inline_agents_enabled_params import (
    BetaManagedAgentsMultiagentInlineAgentsEnabledParams,
)
from .beta_managed_agents_multiagent_inline_agents_disabled_params import (
    BetaManagedAgentsMultiagentInlineAgentsDisabledParams,
)

__all__ = ["BetaManagedAgentsMultiagentInlineAgentsParams"]

BetaManagedAgentsMultiagentInlineAgentsParams: TypeAlias = Union[
    BetaManagedAgentsMultiagentInlineAgentsEnabledParams, BetaManagedAgentsMultiagentInlineAgentsDisabledParams
]
"""Whether the agent can define inline agents.

The agent defines an inline agent itself, in a workflow run's plan or when it spawns a session thread, and the inline agent is not saved.
"""
