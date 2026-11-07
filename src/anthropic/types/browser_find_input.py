from typing import Optional

from .._models import BaseModel

__all__ = ["BrowserFindInput"]


class BrowserFindInput(BaseModel):
    """Find elements matching a natural-language description (e.g.

    "search bar", "add to
    cart button") and return up to 20 matches with element references.
    """

    query: str
    """Natural-language description of the element(s) to find."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
