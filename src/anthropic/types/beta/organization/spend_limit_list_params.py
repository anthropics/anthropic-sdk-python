from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["SpendLimitListParams"]


class SpendLimitListParams(TypedDict, total=False):
    limit: int
    """Maximum number of limits per page. Defaults to `20`."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page` field."""

    scope_type: Optional[
        List[
            Literal[
                "organization", "organization_service", "rbac_group", "seat_tier", "usage_tier", "user", "workspace"
            ]
        ]
    ]
    """Return only limits with these scope types.

    Omit for all. A scope type that doesn't apply to the organization gets a 400
    error.
    """

    workspace_id: Optional[str]
    """
    Return only the limits whose `scope.workspace_id` is this workspace
    (`wrkspc_...`). Claude Console organizations only; other organizations get a 400
    error.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `spend-limit-reads-2026-09-26` in
    this header.
    """
