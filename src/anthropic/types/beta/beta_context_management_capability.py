from typing import Optional

from ..._models import BaseModel
from .beta_capability_support import BetaCapabilitySupport

__all__ = ["BetaContextManagementCapability"]


class BetaContextManagementCapability(BaseModel):
    """Context management capability details."""

    clear_thinking_20251015: Optional[BetaCapabilitySupport] = None
    """Whether the clear_thinking_20251015 strategy is supported."""

    clear_tool_uses_20250919: Optional[BetaCapabilitySupport] = None
    """Whether the clear_tool_uses_20250919 strategy is supported."""

    compact_20260112: Optional[BetaCapabilitySupport] = None
    """Whether the compact_20260112 strategy is supported."""

    supported: bool
    """Whether this capability is supported by the model."""
