# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ....._models import BaseModel
from .beta_workspace_rate_limit_value import BetaWorkspaceRateLimitValue

__all__ = ["BetaWorkspaceRateLimit"]


class BetaWorkspaceRateLimit(BaseModel):
    group_type: Literal["batch", "files", "model_group", "skills", "token_count", "web_search"]
    """The kind of rate-limit group this entry represents.

    `model_group` entries apply to a family of models (listed in `models`); other
    values apply to an API-surface category and have `models` set to `null`.
    """

    limits: List[BetaWorkspaceRateLimitValue]
    """The limiter values overridden for this group in this workspace.

    Limiter types without a workspace override are omitted and inherit the
    organization value.
    """

    models: Optional[List[str]] = None
    """Model names this entry's limits apply to, including aliases.

    `null` when `group_type` is not `"model_group"`.
    """

    rate_limit_id: str
    """The `id` of the RateLimit group this override applies to."""

    type: Literal["workspace_rate_limit"]
    """Object type. Always `workspace_rate_limit` for workspace rate-limit entries."""

    workspace_id: str
    """ID of the Workspace this override applies to."""
