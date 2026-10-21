from typing import Optional

from ..._models import BaseModel
from .beta_browser_click_target import BetaBrowserClickTarget

__all__ = ["BetaBrowserHoverInput"]


class BetaBrowserHoverInput(BaseModel):
    """Move the cursor to a coordinate or element without clicking."""

    target: BetaBrowserClickTarget
    """Where to act: either a viewport coordinate or an element reference."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
