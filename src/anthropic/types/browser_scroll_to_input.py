from typing import Optional

from .._models import BaseModel
from .browser_ref_target import BrowserRefTarget

__all__ = ["BrowserScrollToInput"]


class BrowserScrollToInput(BaseModel):
    """Scroll an element into view."""

    target: BrowserRefTarget
    """
    An element on the page, identified by a reference from a prior `read_page` or
    `find` result. References are scoped to the tab that produced them and become
    stale after navigation or a major re-render.
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
