from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["CacheMissPreviousMessageNotFound"]


class CacheMissPreviousMessageNotFound(BaseModel):
    type: Literal["previous_message_not_found"]
