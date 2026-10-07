from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserWaitInput"]


class BetaBrowserWaitInput(BaseModel):
    """Pause for the given duration."""

    duration: float
    """Seconds to wait (maximum 30)."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
