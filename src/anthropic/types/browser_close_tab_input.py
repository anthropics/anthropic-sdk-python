from .._models import BaseModel

__all__ = ["BrowserCloseTabInput"]


class BrowserCloseTabInput(BaseModel):
    """Close the tab with the given tab_id."""

    tab_id: str
    """The tab to close."""
