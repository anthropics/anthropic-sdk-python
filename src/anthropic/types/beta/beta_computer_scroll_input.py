from typing import List, Optional

from ..._models import BaseModel
from .beta_computer_scroll_direction import BetaComputerScrollDirection

__all__ = ["BetaComputerScrollInput"]


class BetaComputerScrollInput(BaseModel):
    """
    Scroll the screen at the specified (x, y) pixel coordinate, or the current cursor
    position if `coordinate` is omitted. Do NOT use PageUp/PageDown to scroll.
    """

    scroll_amount: int
    """Number of 'clicks' of the scroll wheel."""

    scroll_direction: BetaComputerScrollDirection

    coordinate: Optional[List[int]] = None
    """(x, y): x pixels from the left edge, y pixels from the top edge."""

    text: Optional[str] = None
    """Optional key combination to hold down during this action (e.g.

    "ctrl", "shift", "ctrl+shift").
    """
