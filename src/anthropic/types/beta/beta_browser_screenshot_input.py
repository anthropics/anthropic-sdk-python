from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserScreenshotInput"]


class BetaBrowserScreenshotInput(BaseModel):
    """Capture the current browser viewport."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
