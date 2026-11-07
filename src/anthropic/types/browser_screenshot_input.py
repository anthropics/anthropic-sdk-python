from typing import Optional

from .._models import BaseModel

__all__ = ["BrowserScreenshotInput"]


class BrowserScreenshotInput(BaseModel):
    """Capture the current browser viewport."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
