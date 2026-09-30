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
        List[Literal["organization", "organization_service", "rbac_group", "seat_tier", "user", "workspace"]]
    ]
    """Return only limits with these scope types.

    A Claude Console organization has `organization` and `workspace` limits; a
    Claude Enterprise organization has `organization`, `seat_tier`, `rbac_group`,
    `organization_service` and `user` limits. Omit for all.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `spend-limit-reads-2026-09-26` in
    this header.
    """
