from typing import Optional

from ..._models import BaseModel
from .beta_browser_scroll_direction import BetaBrowserScrollDirection
from .beta_browser_coordinate_target import BetaBrowserCoordinateTarget

__all__ = ["BetaBrowserScrollInput"]


class BetaBrowserScrollInput(BaseModel):
    """Scroll at a viewport position. `target` must be a coordinate target."""

    scroll_direction: BetaBrowserScrollDirection

    target: BetaBrowserCoordinateTarget
    """
    A point in the browser viewport, in viewport pixels (the same frame as a
    full-viewport screenshot).
    """

    scroll_amount: Optional[int] = None
    """Scroll-wheel notches (1–10). Default 3."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
