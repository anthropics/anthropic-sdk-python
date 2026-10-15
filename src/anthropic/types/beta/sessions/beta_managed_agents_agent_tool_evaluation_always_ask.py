from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentToolEvaluationAlwaysAsk"]


class BetaManagedAgentsAgentToolEvaluationAlwaysAsk(BaseModel):
    """
    The resolved permission_policy was always_ask; accompanies evaluated_permission "ask".
    """

    type: Literal["always_ask"]
