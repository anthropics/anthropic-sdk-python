from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent_workflows_enabled import BetaManagedAgentsMultiagentWorkflowsEnabled
from .beta_managed_agents_multiagent_workflows_disabled import BetaManagedAgentsMultiagentWorkflowsDisabled

__all__ = ["BetaManagedAgentsMultiagentWorkflows"]

BetaManagedAgentsMultiagentWorkflows: TypeAlias = Annotated[
    Union[BetaManagedAgentsMultiagentWorkflowsEnabled, BetaManagedAgentsMultiagentWorkflowsDisabled],
    UnionDiscriminator("type"),
]
