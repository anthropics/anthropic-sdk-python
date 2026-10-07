from ..._models import BaseModel

__all__ = ["BetaComputerTypeInput"]


class BetaComputerTypeInput(BaseModel):
    """Type a string of text on the keyboard."""

    text: str
    """The text to type."""
