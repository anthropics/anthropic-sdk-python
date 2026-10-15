from typing_extensions import Literal

from ..._models import BaseModel
from .beta_message import BetaMessage

__all__ = ["BetaRawMessageStartEvent"]


class BetaRawMessageStartEvent(BaseModel):
    message: BetaMessage

    type: Literal["message_start"]
