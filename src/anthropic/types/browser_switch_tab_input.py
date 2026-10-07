from .._models import BaseModel

__all__ = ["BrowserSwitchTabInput"]


class BrowserSwitchTabInput(BaseModel):
    """
    Make the tab with the given tab_id the active tab — the tab that actions without
    a tab_id apply to.
    """

    tab_id: str
    """The tab to switch to."""
