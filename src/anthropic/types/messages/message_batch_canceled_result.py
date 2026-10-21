from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["MessageBatchCanceledResult"]


class MessageBatchCanceledResult(BaseModel):
    type: Literal["canceled"]
