from ..._models import BaseModel

__all__ = ["BetaComputerWaitInput"]


class BetaComputerWaitInput(BaseModel):
    """Wait for a specified duration."""

    duration: int
    """Duration to wait, in seconds."""
