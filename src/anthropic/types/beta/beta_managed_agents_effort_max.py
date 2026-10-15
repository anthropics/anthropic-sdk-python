from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEffortMax"]


class BetaManagedAgentsEffortMax(BaseModel):
    """Maximum effort. Favors reasoning depth over latency."""

    type: Literal["max"]
