from typing import Optional

from .._models import BaseModel
from .browser_ref_target import BrowserRefTarget
from .browser_form_input_value import BrowserFormInputValue

__all__ = ["BrowserFormInputInput"]


class BrowserFormInputInput(BaseModel):
    """Set the value of a form element (input, textarea, select, checkbox).

    Use a
    boolean for checkboxes, an option value or text for selects.
    """

    target: BrowserRefTarget
    """
    An element on the page, identified by a reference from a prior `read_page` or
    `find` result. References are scoped to the tab that produced them and become
    stale after navigation or a major re-render.
    """

    value: BrowserFormInputValue
    """The value to set."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
