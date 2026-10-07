from typing import List, Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserZoomInput"]


class BetaBrowserZoomInput(BaseModel):
    """
    Return a cropped screenshot of the given viewport region, scaled up for closer
    inspection — useful for small icons, buttons, or text. Coordinates are in the
    same viewport-pixel space as a full screenshot.
    """

    region: List[int]
    """[x0, y0, x1, y1] in viewport pixels."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
