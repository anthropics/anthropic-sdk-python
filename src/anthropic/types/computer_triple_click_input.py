from typing import List, Optional

from .._models import BaseModel

__all__ = ["ComputerTripleClickInput"]


class ComputerTripleClickInput(BaseModel):
    """
    Triple-click the left mouse button at the specified (x, y) pixel coordinate, or
    the current cursor position if `coordinate` is omitted.
    """

    coordinate: Optional[List[int]] = None
    """(x, y): x pixels from the left edge, y pixels from the top edge."""

    text: Optional[str] = None
    """Optional key combination to hold down during this action (e.g.

    "ctrl", "shift", "ctrl+shift").
    """
