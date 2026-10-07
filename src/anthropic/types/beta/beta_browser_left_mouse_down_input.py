from typing import Optional

from ..._models import BaseModel
from .beta_browser_coordinate_target import BetaBrowserCoordinateTarget

__all__ = ["BetaBrowserLeftMouseDownInput"]


class BetaBrowserLeftMouseDownInput(BaseModel):
    """Press and hold the left mouse button at a viewport coordinate.

    Pair with
    left_mouse_up to perform a custom drag.
    """

    target: BetaBrowserCoordinateTarget
    """
    A point in the browser viewport, in viewport pixels (the same frame as a
    full-viewport screenshot).
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
