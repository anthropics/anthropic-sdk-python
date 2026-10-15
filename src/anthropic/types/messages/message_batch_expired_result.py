from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["MessageBatchExpiredResult"]


class MessageBatchExpiredResult(BaseModel):
    type: Literal["expired"]
