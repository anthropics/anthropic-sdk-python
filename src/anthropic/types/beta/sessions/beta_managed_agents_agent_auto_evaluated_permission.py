from typing import Union
from typing_extensions import Annotated, TypeAlias

from ...._models import UnionDiscriminator
from .beta_managed_agents_agent_auto_evaluated_permission_ask import BetaManagedAgentsAgentAutoEvaluatedPermissionAsk
from .beta_managed_agents_agent_auto_evaluated_permission_deny import BetaManagedAgentsAgentAutoEvaluatedPermissionDeny
from .beta_managed_agents_agent_auto_evaluated_permission_allow import (
    BetaManagedAgentsAgentAutoEvaluatedPermissionAllow,
)

__all__ = ["BetaManagedAgentsAgentAutoEvaluatedPermission"]

BetaManagedAgentsAgentAutoEvaluatedPermission: TypeAlias = Annotated[
    Union[
        BetaManagedAgentsAgentAutoEvaluatedPermissionAllow,
        BetaManagedAgentsAgentAutoEvaluatedPermissionAsk,
        BetaManagedAgentsAgentAutoEvaluatedPermissionDeny,
    ],
    UnionDiscriminator("type"),
]
"""The server's per-invocation judgement under the auto permission policy.

Its type always equals the event's top-level evaluated_permission. Open union: clients must tolerate unknown variants.
"""
