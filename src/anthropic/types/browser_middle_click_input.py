from typing import Optional

from .._models import BaseModel
from .browser_click_target import BrowserClickTarget

__all__ = ["BrowserMiddleClickInput"]


class BrowserMiddleClickInput(BaseModel):
    """Middle-click at a viewport coordinate or on an element by reference."""

    target: BrowserClickTarget
    """Where to act: either a viewport coordinate or an element reference."""

    modifiers: Optional[str] = None
    """Optional modifier key chord to hold for the duration of this action (e.g.

    "shift", "ctrl+shift", "cmd+alt").
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
