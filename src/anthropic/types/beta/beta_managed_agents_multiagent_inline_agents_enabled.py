from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMultiagentInlineAgentsEnabled"]


class BetaManagedAgentsMultiagentInlineAgentsEnabled(BaseModel):
    """The agent can define inline agents."""

    type: Literal["enabled"]
