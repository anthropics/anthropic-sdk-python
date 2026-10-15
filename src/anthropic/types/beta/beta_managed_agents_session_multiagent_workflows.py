from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._models import UnionDiscriminator
from .beta_managed_agents_multiagent_workflows_disabled import BetaManagedAgentsMultiagentWorkflowsDisabled
from .beta_managed_agents_session_multiagent_workflows_enabled import BetaManagedAgentsSessionMultiagentWorkflowsEnabled

__all__ = ["BetaManagedAgentsSessionMultiagentWorkflows"]

BetaManagedAgentsSessionMultiagentWorkflows: TypeAlias = Annotated[
    Union[BetaManagedAgentsSessionMultiagentWorkflowsEnabled, BetaManagedAgentsMultiagentWorkflowsDisabled],
    UnionDiscriminator("type"),
]
