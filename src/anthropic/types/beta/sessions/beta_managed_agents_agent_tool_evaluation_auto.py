from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_agent_auto_evaluated_permission import BetaManagedAgentsAgentAutoEvaluatedPermission

__all__ = ["BetaManagedAgentsAgentToolEvaluationAuto"]


class BetaManagedAgentsAgentToolEvaluationAuto(BaseModel):
    """
    The resolved permission_policy was auto: the server judged this invocation individually.
    """

    evaluated_permission: BetaManagedAgentsAgentAutoEvaluatedPermission
    """The server's per-invocation judgement under the auto permission policy.

    Its type always equals the event's top-level evaluated_permission. Open union:
    clients must tolerate unknown variants.
    """

    type: Literal["auto"]
