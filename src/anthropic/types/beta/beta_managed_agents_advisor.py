from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAdvisor"]


class BetaManagedAgentsAdvisor(BaseModel):
    """
    Platform advisor roster entry: a model the session's primary thread may consult mid-turn.
    """

    model: str
    """The advisor model id."""

    type: Literal["advisor"]
