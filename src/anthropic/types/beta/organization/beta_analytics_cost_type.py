from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsCostType"]

BetaAnalyticsCostType: TypeAlias = Literal["code_execution", "tokens", "web_search"]
