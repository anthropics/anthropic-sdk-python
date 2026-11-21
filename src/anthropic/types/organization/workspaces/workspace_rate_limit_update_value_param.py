from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .workspace_rate_limit_type import WorkspaceRateLimitType

__all__ = ["WorkspaceRateLimitUpdateValueParam"]


class WorkspaceRateLimitUpdateValueParam(TypedDict, total=False):
    type: Required[WorkspaceRateLimitType]
    """Rate limiter type.

    `input_tokens_per_minute` counts every input token, cache reads included.
    `input_tokens_per_minute_cache_aware` does not count cache reads, and on current
    models the organization's input-token limit usually has this type. A workspace
    limit of either type applies alongside the organization's limit, not in place of
    it. Because cache reads count toward an `input_tokens_per_minute` limit, it can
    reject requests that read mostly from the cache while the organization's limit
    still has room.
    """

    value: Required[Optional[int]]
    """New limit value.

    Set to null to clear the workspace override and fall back to the organization
    limit.
    """
