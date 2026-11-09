from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMultiagentSubagentsDisabled"]


class BetaManagedAgentsMultiagentSubagentsDisabled(BaseModel):
    """The agent cannot spawn session threads."""

    type: Literal["disabled"]
