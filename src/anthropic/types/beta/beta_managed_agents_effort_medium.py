from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEffortMedium"]


class BetaManagedAgentsEffortMedium(BaseModel):
    """Medium effort. Balances latency and reasoning depth."""

    type: Literal["medium"]
