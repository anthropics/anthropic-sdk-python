from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SpendLimitOrganizationScope"]


class SpendLimitOrganizationScope(BaseModel):
    type: Literal["organization"]
