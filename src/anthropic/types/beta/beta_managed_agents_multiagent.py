from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent20261001 import BetaManagedAgentsMultiagent20261001
from .beta_managed_agents_multiagent_coordinator import BetaManagedAgentsMultiagentCoordinator

__all__ = ["BetaManagedAgentsMultiagent"]

BetaManagedAgentsMultiagent: TypeAlias = Annotated[
    Union[BetaManagedAgentsMultiagentCoordinator, BetaManagedAgentsMultiagent20261001], UnionDiscriminator("type")
]
