from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitOrganizationScope"]


class BetaSpendLimitOrganizationScope(BaseModel):
    type: Literal["organization"]
