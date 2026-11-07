from typing import List

from ..._models import BaseModel

__all__ = ["BetaComputerZoomInput"]


class BetaComputerZoomInput(BaseModel):
    """Take a screenshot of a rectangular region.

    Region coordinates are in the
    full-screenshot space (not physical display pixels). The crop is scaled up to
    fill the image budget so fine details become legible.
    """

    region: List[int]
    """(x0, y0, x1, y1): The region to capture."""
