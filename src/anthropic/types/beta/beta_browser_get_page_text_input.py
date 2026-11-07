from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserGetPageTextInput"]


class BetaBrowserGetPageTextInput(BaseModel):
    """
    Return the page's visible text content as plain text, prioritizing article
    content. Suited to articles, documentation, and other text-heavy pages.
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
