from typing_extensions import Literal, TypeAlias

__all__ = ["SpendLimitPeriod"]

SpendLimitPeriod: TypeAlias = Literal["daily", "monthly", "weekly"]
