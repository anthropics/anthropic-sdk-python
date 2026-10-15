from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentAutoEvaluatedPermissionAsk"]


class BetaManagedAgentsAgentAutoEvaluatedPermissionAsk(BaseModel):
    """The server reached no judgement; the invocation is held for client approval."""

    reason_code: str
    """
    The judgement's grounds in registry-bound terms, for client branching and audit
    rather than end-user display. Open registry; currently "indeterminate" (no
    judgement was reached). Clients must tolerate values outside this set.
    """

    type: Literal["ask"]
