from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaCacheMissUnavailable"]


class BetaCacheMissUnavailable(BaseModel):
    type: Literal["unavailable"]
