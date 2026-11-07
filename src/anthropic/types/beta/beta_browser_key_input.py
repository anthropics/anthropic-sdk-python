from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserKeyInput"]


class BetaBrowserKeyInput(BaseModel):
    """Press a key or key chord.

    Use "+" to combine modifiers with a key (e.g. "ctrl+a",
    "cmd+shift+p") and space to sequence presses (e.g. "Backspace Backspace Delete").
    Common names like "Return", "Tab", "Escape", "BackSpace" are supported.
    """

    text: str
    """The key, chord, or space-separated sequence to press."""

    repeat: Optional[int] = None
    """Number of times to repeat. Default 1."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
