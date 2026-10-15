from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaMessageBatchExpiredResult"]


class BetaMessageBatchExpiredResult(BaseModel):
    type: Literal["expired"]
