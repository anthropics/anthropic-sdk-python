from typing import Optional

from .._models import BaseModel

__all__ = ["BrowserReadConsoleInput"]


class BrowserReadConsoleInput(BaseModel):
    """
    Return console output (log entries, errors, warnings) accumulated since the
    driver attached to the tab and since the last read, one line per entry. An empty
    result does not mean no traffic for a tab that predates attach.
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
