from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsSessionEndTurn"]


class BetaManagedAgentsSessionEndTurn(BaseModel):
    """The agent completed its turn naturally and is ready for the next user message."""

    type: Literal["end_turn"]
