from ..._models import BaseModel
from .beta_capability_support import BetaCapabilitySupport

__all__ = ["BetaCompactionCapability"]


class BetaCompactionCapability(BaseModel):
    """
    Compaction capability details: whether the model accepts the top-level
    `compaction` request parameter, with one entry per supported
    `compaction.type` value.
    """

    summarize: BetaCapabilitySupport
    """Whether the summarize compaction type is supported."""

    supported: bool
    """Whether this capability is supported by the model."""
