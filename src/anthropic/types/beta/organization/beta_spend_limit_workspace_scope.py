from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitWorkspaceScope"]


class BetaSpendLimitWorkspaceScope(BaseModel):
    """Scope selecting one workspace of a Claude Console organization."""

    type: Literal["workspace"]
    """Scope type. Always `workspace` for this scope."""

    workspace_id: str
    """Tagged ID of the workspace the spend limit applies to."""
