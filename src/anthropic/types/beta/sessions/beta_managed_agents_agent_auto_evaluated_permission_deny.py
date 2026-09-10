from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentAutoEvaluatedPermissionDeny"]


class BetaManagedAgentsAgentAutoEvaluatedPermissionDeny(BaseModel):
    """
    The server judged the invocation high-risk; it does not execute and a synthetic error tool result is appended.
    """

    reason_code: str
    """The judgement's grounds in registry-bound terms.

    Open registry; currently "high_risk" (judged high-risk; the call does not run).
    Clients must tolerate values outside this set.
    """

    type: Literal["deny"]
