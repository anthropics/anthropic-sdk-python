from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsGroupedCostType"]

BetaAnalyticsGroupedCostType: TypeAlias = Literal["code_execution", "session_usage", "tokens", "web_search"]
