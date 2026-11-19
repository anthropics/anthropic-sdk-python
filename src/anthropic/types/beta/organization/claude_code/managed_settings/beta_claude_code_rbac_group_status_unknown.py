from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeCodeRBACGroupStatusUnknown"]


class BetaClaudeCodeRBACGroupStatusUnknown(BaseModel):
    type: Literal["unknown"]
    """Always `unknown`."""
