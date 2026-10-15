from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsRetryStatusExhausted"]


class BetaManagedAgentsRetryStatusExhausted(BaseModel):
    """This turn is dead; queued inputs are flushed and the session returns to idle.

    Client may send a new prompt.
    """

    type: Literal["exhausted"]
