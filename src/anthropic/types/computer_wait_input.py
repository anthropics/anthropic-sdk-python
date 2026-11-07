from .._models import BaseModel

__all__ = ["ComputerWaitInput"]


class ComputerWaitInput(BaseModel):
    """Wait for a specified duration."""

    duration: int
    """Duration to wait, in seconds."""
