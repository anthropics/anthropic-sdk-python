from typing_extensions import Literal, TypeAlias

__all__ = ["SpendLimitIncreaseRequestStatus"]

SpendLimitIncreaseRequestStatus: TypeAlias = Literal["approved", "denied", "pending"]
