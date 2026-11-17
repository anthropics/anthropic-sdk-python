from typing_extensions import Literal

from ..._exceptions import RateLimitError
from .contract_spend_limit_reached_error_details import ContractSpendLimitReachedErrorDetails

__all__ = ["ContractSpendLimitReachedError"]


class ContractSpendLimitReachedError(RateLimitError):
    """The organization has reached the spend limit of its contract."""

    error_code: Literal["contract_spend_limit_reached"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: ContractSpendLimitReachedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
