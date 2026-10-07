from .._models import BaseModel

__all__ = ["ComputerTypeInput"]


class ComputerTypeInput(BaseModel):
    """Type a string of text on the keyboard."""

    text: str
    """The text to type."""
