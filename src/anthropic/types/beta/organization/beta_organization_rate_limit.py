# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_organization_rate_limit_value import BetaOrganizationRateLimitValue

__all__ = ["BetaOrganizationRateLimit"]


class BetaOrganizationRateLimit(BaseModel):
    id: str
    """Stable identifier for this rate-limit group within the organization."""

    group_type: Literal["batch", "files", "model_group", "skills", "token_count", "web_search"]
    """The kind of rate-limit group this entry represents.

    `model_group` entries apply to a family of models (listed in `models`); other
    values apply to an API-surface category and have `models` set to `null`.
    """

    limits: List[BetaOrganizationRateLimitValue]
    """The limiter values that apply to this group."""

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group_type` is not `"model_group"`.
    """

    type: Literal["rate_limit"]
    """Object type. Always `rate_limit` for organization rate-limit entries."""
