# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ....._models import BaseModel

__all__ = ["BetaWorkspaceRateLimitValue"]


class BetaWorkspaceRateLimitValue(BaseModel):
    org_limit: Optional[int] = None
    """The organization-level value for the same limiter type, for reference.

    `null` when the organization has no limit configured for this limiter type.
    """

    type: str
    """
    The limiter type (for example, `requests_per_minute` or
    `input_tokens_per_minute`).
    """

    value: int
    """The workspace-level override value for this limiter type."""
