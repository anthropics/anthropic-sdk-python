from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .workspace_rate_limit_type import WorkspaceRateLimitType

__all__ = ["WorkspaceRateLimitUpdateValueParam"]


class WorkspaceRateLimitUpdateValueParam(TypedDict, total=False):
    type: Required[WorkspaceRateLimitType]
    """Rate limiter type."""

    value: Required[Optional[int]]
    """New limit value.

    Set to null to clear the workspace override and fall back to the organization
    limit.
    """
