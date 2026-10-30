from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["SpendLimitOrganizationServiceScope"]


class SpendLimitOrganizationServiceScope(BaseModel):
    service: str

    type: Literal["organization_service"]
