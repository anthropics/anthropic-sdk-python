from typing_extensions import Literal

from .message import Message
from .._models import BaseModel

__all__ = ["RawMessageStartEvent"]


class RawMessageStartEvent(BaseModel):
    message: Message

    type: Literal["message_start"]
