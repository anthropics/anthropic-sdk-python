from typing_extensions import Literal, TypeAlias

__all__ = ["BetaSpendLimitIncreaseRequestStatus"]

BetaSpendLimitIncreaseRequestStatus: TypeAlias = Literal["approved", "denied", "pending"]
