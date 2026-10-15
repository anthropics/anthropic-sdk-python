from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMultiagentAdvisorDisabled"]


class BetaManagedAgentsMultiagentAdvisorDisabled(BaseModel):
    """The agent has no advisor."""

    type: Literal["disabled"]
