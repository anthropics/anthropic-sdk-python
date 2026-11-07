from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitUsageTierScope"]


class BetaSpendLimitUsageTierScope(BaseModel):
    """
    Scope of the monthly spend cap Anthropic sets for a Claude Console
    organization from its usage tier, or a higher cap Anthropic granted the
    organization. Read-only; its `created_at` and `updated_at` are the
    organization's creation time, so `amount` can change while `updated_at` stays
    the same.
    """

    type: Literal["usage_tier"]
    """Scope type. Always `usage_tier` for this scope."""
