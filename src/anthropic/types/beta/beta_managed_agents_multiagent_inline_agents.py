from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent_inline_agents_enabled import BetaManagedAgentsMultiagentInlineAgentsEnabled
from .beta_managed_agents_multiagent_inline_agents_disabled import BetaManagedAgentsMultiagentInlineAgentsDisabled

__all__ = ["BetaManagedAgentsMultiagentInlineAgents"]

BetaManagedAgentsMultiagentInlineAgents: TypeAlias = Annotated[
    Union[BetaManagedAgentsMultiagentInlineAgentsEnabled, BetaManagedAgentsMultiagentInlineAgentsDisabled],
    UnionDiscriminator("type"),
]
"""Whether the agent can define inline agents.

The agent defines an inline agent itself, in a workflow run's plan or when it spawns a session thread, and the inline agent is not saved.
"""
