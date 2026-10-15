from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_program_workflow_run_error import BetaManagedAgentsProgramWorkflowRunError
from .beta_managed_agents_timeout_workflow_run_error import BetaManagedAgentsTimeoutWorkflowRunError
from .beta_managed_agents_unknown_workflow_run_error import BetaManagedAgentsUnknownWorkflowRunError
from .beta_managed_agents_thread_limit_workflow_run_error import BetaManagedAgentsThreadLimitWorkflowRunError
from .beta_managed_agents_max_workflow_runs_workflow_run_error import BetaManagedAgentsMaxWorkflowRunsWorkflowRunError

__all__ = ["BetaManagedAgentsWorkflowRunError"]

BetaManagedAgentsWorkflowRunError: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsTimeoutWorkflowRunError,
        BetaManagedAgentsProgramWorkflowRunError,
        BetaManagedAgentsUnknownWorkflowRunError,
        BetaManagedAgentsThreadLimitWorkflowRunError,
        BetaManagedAgentsMaxWorkflowRunsWorkflowRunError,
    ],
    UnionDiscriminator("type"),
]
