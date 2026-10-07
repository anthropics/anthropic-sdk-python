from typing import Optional

from .._models import BaseModel

__all__ = ["ComputerKeyInput"]


class ComputerKeyInput(BaseModel):
    """Press a key or key-combination on the keyboard.

    Use "+" to combine modifiers with
    a key (e.g. "ctrl+s", "alt+Tab", "ctrl+shift+Escape"). Key names are
    case-insensitive; common names like "Return", "Tab", "Escape", "Up", "Down",
    "Left", "Right", "Home", "End", "Page_Up", "Page_Down", "Delete", "BackSpace" are
    supported.
    """

    text: str
    """The key or key-combination to press."""

    repeat: Optional[int] = None
    """Number of times to repeat the key press. Default is 1."""
