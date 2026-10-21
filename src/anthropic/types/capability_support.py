from .._models import BaseModel

__all__ = ["CapabilitySupport"]


class CapabilitySupport(BaseModel):
    """Indicates whether a capability is supported."""

    supported: bool
    """Whether this capability is supported by the model."""
