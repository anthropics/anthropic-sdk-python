from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent_subagents_disabled import BetaManagedAgentsMultiagentSubagentsDisabled
from .beta_managed_agents_session_multiagent_subagents_enabled import BetaManagedAgentsSessionMultiagentSubagentsEnabled

__all__ = ["BetaManagedAgentsSessionMultiagentSubagents"]

BetaManagedAgentsSessionMultiagentSubagents: TypeAlias = Annotated[
    Union[BetaManagedAgentsSessionMultiagentSubagentsEnabled, BetaManagedAgentsMultiagentSubagentsDisabled],
    UnionDiscriminator("type"),
]
