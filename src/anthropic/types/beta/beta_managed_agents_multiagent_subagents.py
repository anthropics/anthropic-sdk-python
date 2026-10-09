from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent_subagents_enabled import BetaManagedAgentsMultiagentSubagentsEnabled
from .beta_managed_agents_multiagent_subagents_disabled import BetaManagedAgentsMultiagentSubagentsDisabled

__all__ = ["BetaManagedAgentsMultiagentSubagents"]

BetaManagedAgentsMultiagentSubagents: TypeAlias = Annotated[
    Union[BetaManagedAgentsMultiagentSubagentsEnabled, BetaManagedAgentsMultiagentSubagentsDisabled],
    UnionDiscriminator("type"),
]
