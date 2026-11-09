from typing import List, Optional

from .._models import BaseModel

__all__ = ["ComputerLeftClickDragInput"]


class ComputerLeftClickDragInput(BaseModel):
    """Click and drag the cursor from `start_coordinate` to `coordinate`."""

    coordinate: List[int]
    """(x, y): x pixels from the left edge, y pixels from the top edge."""

    start_coordinate: List[int]
    """(x, y): x pixels from the left edge, y pixels from the top edge."""

    text: Optional[str] = None
    """Optional key combination to hold down during this action (e.g.

    "ctrl", "shift", "ctrl+shift").
    """
