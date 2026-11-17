from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ContractSpendLimitReachedErrorDetails"]


class ContractSpendLimitReachedErrorDetails(BaseModel):
    """The organization has reached the spend limit of its contract."""

    error_code: Literal["contract_spend_limit_reached"]
