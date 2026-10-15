from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaCacheMissPreviousMessageNotFound"]


class BetaCacheMissPreviousMessageNotFound(BaseModel):
    type: Literal["previous_message_not_found"]
