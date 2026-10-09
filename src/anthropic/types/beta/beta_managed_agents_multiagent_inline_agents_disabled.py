from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMultiagentInlineAgentsDisabled"]


class BetaManagedAgentsMultiagentInlineAgentsDisabled(BaseModel):
    """The agent cannot define inline agents."""

    type: Literal["disabled"]
