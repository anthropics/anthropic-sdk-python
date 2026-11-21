from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeCodeRBACGroupStatusDeleted"]


class BetaClaudeCodeRBACGroupStatusDeleted(BaseModel):
    type: Literal["deleted"]
    """Always `deleted`."""
