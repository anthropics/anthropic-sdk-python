from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent_advisor_enabled import BetaManagedAgentsMultiagentAdvisorEnabled
from .beta_managed_agents_multiagent_advisor_disabled import BetaManagedAgentsMultiagentAdvisorDisabled

__all__ = ["BetaManagedAgentsMultiagentAdvisor"]

BetaManagedAgentsMultiagentAdvisor: TypeAlias = Annotated[
    Union[BetaManagedAgentsMultiagentAdvisorEnabled, BetaManagedAgentsMultiagentAdvisorDisabled],
    UnionDiscriminator("type"),
]
