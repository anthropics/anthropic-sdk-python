from typing_extensions import Literal, TypeAlias

__all__ = ["BetaAnalyticsOrder"]

BetaAnalyticsOrder: TypeAlias = Literal["asc", "desc"]
"""Sort direction: `asc` or `desc`.

Defaults to `asc` for the endpoint's sort column and to `desc` when `order_by` names a metric (a top-N ranking). Applies to `order_by`, or to the endpoint's default sort field when `order_by` is omitted.
"""
