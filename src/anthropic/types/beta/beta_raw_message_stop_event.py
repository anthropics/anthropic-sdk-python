from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaRawMessageStopEvent"]


class BetaRawMessageStopEvent(BaseModel):
    type: Literal["message_stop"]
