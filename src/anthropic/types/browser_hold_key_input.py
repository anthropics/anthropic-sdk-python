from typing import Optional

from .._models import BaseModel

__all__ = ["BrowserHoldKeyInput"]


class BrowserHoldKeyInput(BaseModel):
    """Hold a key or key chord down for a duration, then release it.

    Uses the same key
    names and "+" chord syntax as the key action.
    """

    duration: float
    """Seconds to hold the key down (maximum 30)."""

    text: str
    """The key or chord to hold."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
