from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitSeatTierScope"]


class BetaSpendLimitSeatTierScope(BaseModel):
    seat_tier: str

    type: Literal["seat_tier"]
