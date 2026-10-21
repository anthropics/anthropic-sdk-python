from typing import Optional

from .._models import BaseModel
from .browser_read_page_filter import BrowserReadPageFilter

__all__ = ["BrowserReadPageInput"]


class BrowserReadPageInput(BaseModel):
    """
    Return a structured accessibility tree of the page (or the subtree rooted at
    `ref`), with element references like [ref_7] that can be used as targets on later
    actions. Output is capped at 50,000 characters — narrow with `ref` or a smaller
    `depth` when exceeded.
    """

    depth: Optional[int] = None
    """Maximum tree depth. Default 15."""

    filter: Optional[BrowserReadPageFilter] = None
    """Which elements to include.

    Omitted: every visible element. "interactive": interactive elements only. "all":
    additionally includes off-viewport elements.
    """

    ref: Optional[str] = None
    """Element reference to read a subtree from. Omit to read from the page root."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
