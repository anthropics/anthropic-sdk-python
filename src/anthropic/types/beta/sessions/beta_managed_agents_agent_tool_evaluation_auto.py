from typing_extensions import Literal

from ...._models import BaseModel
from .beta_managed_agents_agent_auto_evaluated_permission import BetaManagedAgentsAgentAutoEvaluatedPermission

__all__ = ["BetaManagedAgentsAgentToolEvaluationAuto"]


class BetaManagedAgentsAgentToolEvaluationAuto(BaseModel):
    """
    The resolved permission_policy was auto: the server judged this invocation individually.
    """

    evaluated_permission: BetaManagedAgentsAgentAutoEvaluatedPermission
    """The server's judgement for this invocation."""

    type: Literal["auto"]
