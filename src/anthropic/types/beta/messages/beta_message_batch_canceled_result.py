from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaMessageBatchCanceledResult"]


class BetaMessageBatchCanceledResult(BaseModel):
    type: Literal["canceled"]
