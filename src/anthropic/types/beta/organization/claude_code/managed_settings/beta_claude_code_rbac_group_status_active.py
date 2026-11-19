from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeCodeRBACGroupStatusActive"]


class BetaClaudeCodeRBACGroupStatusActive(BaseModel):
    type: Literal["active"]
    """Always `active`."""
