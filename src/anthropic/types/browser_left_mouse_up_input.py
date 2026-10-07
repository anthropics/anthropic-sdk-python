from typing import Optional

from .._models import BaseModel
from .browser_coordinate_target import BrowserCoordinateTarget

__all__ = ["BrowserLeftMouseUpInput"]


class BrowserLeftMouseUpInput(BaseModel):
    """Release the left mouse button at a viewport coordinate."""

    target: BrowserCoordinateTarget
    """
    A point in the browser viewport, in viewport pixels (the same frame as a
    full-viewport screenshot).
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
