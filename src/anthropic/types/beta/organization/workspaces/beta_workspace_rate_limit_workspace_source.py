from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaWorkspaceRateLimitWorkspaceSource"]


class BetaWorkspaceRateLimitWorkspaceSource(BaseModel):
    type: Literal["workspace"]
    """Always `workspace`: a workspace-level override is stored."""
