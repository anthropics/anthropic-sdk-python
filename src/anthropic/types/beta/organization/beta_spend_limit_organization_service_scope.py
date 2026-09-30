from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitOrganizationServiceScope"]


class BetaSpendLimitOrganizationServiceScope(BaseModel):
    service: str

    type: Literal["organization_service"]
