from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SpendLimitSeatTierScope"]


class SpendLimitSeatTierScope(BaseModel):
    seat_tier: str

    type: Literal["seat_tier"]
