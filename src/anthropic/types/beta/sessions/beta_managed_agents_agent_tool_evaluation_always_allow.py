from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolEvaluationAlwaysAllow"]


class BetaManagedAgentsAgentToolEvaluationAlwaysAllow(BaseModel):
    """
    The resolved permission_policy was always_allow; accompanies evaluated_permission "allow".
    """

    type: Literal["always_allow"]
