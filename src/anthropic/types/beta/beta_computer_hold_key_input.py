from ..._models import BaseModel

__all__ = ["BetaComputerHoldKeyInput"]


class BetaComputerHoldKeyInput(BaseModel):
    """Hold down a key or key-combination for a specified duration.

    Uses the same key
    syntax as `key`.
    """

    duration: int
    """Duration to hold the key, in seconds."""

    text: str
    """The key or key-combination to hold."""
