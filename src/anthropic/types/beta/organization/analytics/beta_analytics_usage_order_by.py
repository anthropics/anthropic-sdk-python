from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsUsageOrderBy"]

BetaAnalyticsUsageOrderBy: TypeAlias = Literal[
    "output_tokens", "requests", "time", "total_tokens", "uncached_input_tokens"
]
