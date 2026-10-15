from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaSpendLimitWorkspaceScopeParam"]


class BetaSpendLimitWorkspaceScopeParam(TypedDict, total=False):
    """Scope selecting one workspace of a Claude Console organization."""

    type: Required[Literal["workspace"]]
    """Scope type. Always `workspace` for this scope."""

    workspace_id: Required[str]
    """Tagged ID of the workspace the spend limit applies to."""
