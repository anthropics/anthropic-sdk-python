from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsAgentAutoEvaluatedPermissionDeny"]


class BetaManagedAgentsAgentAutoEvaluatedPermissionDeny(BaseModel):
    """
    The server judged the invocation high-risk, or reached no judgement and did not hold it for client approval (for example, because the organization is out of credits or has reached a spend limit); it does not execute and a synthetic error tool result is appended.
    """

    reason_code: str
    """The judgement's grounds in registry-bound terms.

    Open registry; currently "high_risk" (judged high-risk; the call does not run)
    and "indeterminate" (no judgement was reached; the call does not run). Clients
    must tolerate values outside this set.
    """

    type: Literal["deny"]
