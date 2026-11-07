from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["RawMessageStopEvent"]


class RawMessageStopEvent(BaseModel):
    type: Literal["message_stop"]
