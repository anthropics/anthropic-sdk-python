from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMultiagentAdvisorEnabled"]


class BetaManagedAgentsMultiagentAdvisorEnabled(BaseModel):
    """The session's primary thread can consult `model` mid-turn."""

    model: str
    """The advisor model id."""

    type: Literal["enabled"]
