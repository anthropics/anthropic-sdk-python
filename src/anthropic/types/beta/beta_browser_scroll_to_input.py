from typing import Optional

from ..._models import BaseModel
from .beta_browser_ref_target import BetaBrowserRefTarget

__all__ = ["BetaBrowserScrollToInput"]


class BetaBrowserScrollToInput(BaseModel):
    """Scroll an element into view."""

    target: BetaBrowserRefTarget
    """
    An element on the page, identified by a reference from a prior `read_page` or
    `find` result. References are scoped to the tab that produced them and become
    stale after navigation or a major re-render.
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
