from typing import Optional

from .._models import BaseModel
from .browser_click_target import BrowserClickTarget

__all__ = ["BrowserHoverInput"]


class BrowserHoverInput(BaseModel):
    """Move the cursor to a coordinate or element without clicking."""

    target: BrowserClickTarget
    """Where to act: either a viewport coordinate or an element reference."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
