from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_managed_agents_aws_role_execution_identity_params import BetaManagedAgentsAWSRoleExecutionIdentityParams
from .beta_managed_agents_service_account_execution_identity_params import (
    BetaManagedAgentsServiceAccountExecutionIdentityParams,
)

__all__ = ["BetaManagedAgentsExecutionIdentityParams"]

BetaManagedAgentsExecutionIdentityParams: TypeAlias = Union[
    BetaManagedAgentsAWSRoleExecutionIdentityParams, BetaManagedAgentsServiceAccountExecutionIdentityParams
]
"""
Execution principal for runs of this agent: `service_account` (the default) or `aws_role`.
"""
