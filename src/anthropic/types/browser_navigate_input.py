from typing import Optional

from .._models import BaseModel

__all__ = ["BrowserNavigateInput"]


class BrowserNavigateInput(BaseModel):
    """Navigate to a URL, or go back/forward/reload in history.

    The protocol may be
    omitted (defaults to https://).
    """

    url: str
    """
    The URL to navigate to, or "back" / "forward" / "reload" for history navigation.
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
