from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

from .workspace_rate_limit_update_value_param import WorkspaceRateLimitUpdateValueParam

__all__ = ["RateLimitUpdateParams"]


class RateLimitUpdateParams(TypedDict, total=False):
    workspace_id: Required[str]
    """The ID of the workspace."""

    limits: Required[Iterable[WorkspaceRateLimitUpdateValueParam]]
    """Limits to set or clear. Unspecified limit types are unchanged."""
