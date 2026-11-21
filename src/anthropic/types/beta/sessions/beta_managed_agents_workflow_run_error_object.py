from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_program_workflow_run_error_object import BetaManagedAgentsProgramWorkflowRunErrorObject
from .beta_managed_agents_timeout_workflow_run_error_object import BetaManagedAgentsTimeoutWorkflowRunErrorObject
from .beta_managed_agents_unknown_workflow_run_error_object import BetaManagedAgentsUnknownWorkflowRunErrorObject
from .beta_managed_agents_thread_limit_workflow_run_error_object import (
    BetaManagedAgentsThreadLimitWorkflowRunErrorObject,
)
from .beta_managed_agents_max_workflow_runs_workflow_run_error_object import (
    BetaManagedAgentsMaxWorkflowRunsWorkflowRunErrorObject,
)

__all__ = ["BetaManagedAgentsWorkflowRunErrorObject"]

BetaManagedAgentsWorkflowRunErrorObject: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsTimeoutWorkflowRunErrorObject,
        BetaManagedAgentsProgramWorkflowRunErrorObject,
        BetaManagedAgentsUnknownWorkflowRunErrorObject,
        BetaManagedAgentsThreadLimitWorkflowRunErrorObject,
        BetaManagedAgentsMaxWorkflowRunsWorkflowRunErrorObject,
    ],
    UnionDiscriminator("type"),
]
