from typing_extensions import Literal

from ...._models import BaseModel
from ..beta_message import BetaMessage

__all__ = ["BetaMessageBatchSucceededResult"]


class BetaMessageBatchSucceededResult(BaseModel):
    message: BetaMessage

    type: Literal["succeeded"]
