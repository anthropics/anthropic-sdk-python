from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaBrowserJavascriptExecInput"]


class BetaBrowserJavascriptExecInput(BaseModel):
    """
    Execute JavaScript in the page context and return the value of the last
    expression. The code runs with access to the DOM, `window`, and page variables.
    Write the expression you want evaluated — do NOT use `return`.
    """

    text: str
    """JavaScript to execute in the page context."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
