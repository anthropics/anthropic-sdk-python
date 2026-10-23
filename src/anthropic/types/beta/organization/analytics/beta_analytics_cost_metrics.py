from typing import Optional

from ....._models import BaseModel

__all__ = ["BetaAnalyticsCostMetrics"]


class BetaAnalyticsCostMetrics(BaseModel):
    """The cost of one row."""

    amount: str
    """Amount (post-discount, pre-credit) in fractional cents (minor units)."""

    currency: str
    """Currency code for the cost amount. Currently always `"USD"`."""

    list_amount: str
    """List-price amount (pre-discount) in fractional cents."""

    requests: Optional[int] = None
    """Number of API requests in this row's scope.

    Null when `group_by` includes `cost_type` or `token_type` (the count has no
    per-component attribution; read it from the ungrouped response). For sandbox /
    code-execution events, this counts execution spans rather than HTTP requests
    (these rows surface with `product: null`).
    """
