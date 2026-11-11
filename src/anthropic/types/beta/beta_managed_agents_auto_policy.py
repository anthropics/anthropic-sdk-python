from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAutoPolicy"]


class BetaManagedAgentsAutoPolicy(BaseModel):
    """
    The server decides each tool call individually: it judges, from the tool, its input, and the session content so far, whether the call is safe to execute or high-risk, and evaluates it to allow when judged safe and to deny when judged high-risk. A call the server cannot reach a judgement on evaluates to ask, or for some causes to deny, for example when the organization is out of credits or has reached a spend limit.
    """

    type: Literal["auto"]
