from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserTypeInput"]


class BetaBrowserTypeInput(BaseModel):
    """Type a literal string at the current focus."""

    text: str
    """The text to type."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
