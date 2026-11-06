from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .beta_workspace_rate_limit_type import BetaWorkspaceRateLimitType

__all__ = ["BetaWorkspaceRateLimitUpdateValueParam"]


class BetaWorkspaceRateLimitUpdateValueParam(TypedDict, total=False):
    type: Required[BetaWorkspaceRateLimitType]
    """Rate limiter type."""

    value: Required[Optional[int]]
    """New limit value.

    Set to null to clear the workspace override and fall back to the organization
    limit.
    """
