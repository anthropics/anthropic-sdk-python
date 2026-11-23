from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_workflow_run_result_stopped import BetaManagedAgentsWorkflowRunResultStopped
from .beta_managed_agents_workflow_run_result_completed import BetaManagedAgentsWorkflowRunResultCompleted
from .beta_managed_agents_workflow_run_result_error_object import BetaManagedAgentsWorkflowRunResultErrorObject

__all__ = ["BetaManagedAgentsWorkflowRunResult"]

BetaManagedAgentsWorkflowRunResult: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsWorkflowRunResultCompleted,
        BetaManagedAgentsWorkflowRunResultErrorObject,
        BetaManagedAgentsWorkflowRunResultStopped,
    ],
    UnionDiscriminator("type"),
]
"""How a workflow run ended."""
