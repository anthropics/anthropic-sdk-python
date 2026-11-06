from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_workflow_run_result_error import BetaManagedAgentsWorkflowRunResultError
from .beta_managed_agents_workflow_run_result_stopped import BetaManagedAgentsWorkflowRunResultStopped
from .beta_managed_agents_workflow_run_result_completed import BetaManagedAgentsWorkflowRunResultCompleted

__all__ = ["BetaManagedAgentsWorkflowRunResult"]

BetaManagedAgentsWorkflowRunResult: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsWorkflowRunResultCompleted,
        BetaManagedAgentsWorkflowRunResultError,
        BetaManagedAgentsWorkflowRunResultStopped,
    ],
    UnionDiscriminator("type"),
]
