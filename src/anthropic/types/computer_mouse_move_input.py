from typing import List

from .._models import BaseModel

__all__ = ["ComputerMouseMoveInput"]


class ComputerMouseMoveInput(BaseModel):
    """Move the cursor to a specified (x, y) pixel coordinate.

    Use this ONLY to hover
    without clicking; otherwise use a click action directly.
    """

    coordinate: List[int]
    """(x, y): x pixels from the left edge, y pixels from the top edge."""
