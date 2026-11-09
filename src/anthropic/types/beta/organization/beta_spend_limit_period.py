from typing_extensions import Literal, TypeAlias

__all__ = ["BetaSpendLimitPeriod"]

BetaSpendLimitPeriod: TypeAlias = Literal["daily", "monthly", "weekly"]
