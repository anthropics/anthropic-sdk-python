from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsServiceTier"]

BetaAnalyticsServiceTier: TypeAlias = Literal[
    "batch", "flex", "flex_discount", "priority", "priority_on_demand", "standard"
]
