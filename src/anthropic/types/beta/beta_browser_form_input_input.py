from typing import Optional

from ..._models import BaseModel
from .beta_browser_ref_target import BetaBrowserRefTarget
from .beta_browser_form_input_value import BetaBrowserFormInputValue

__all__ = ["BetaBrowserFormInputInput"]


class BetaBrowserFormInputInput(BaseModel):
    """Set the value of a form element (input, textarea, select, checkbox).

    Use a
    boolean for checkboxes, an option value or text for selects.
    """

    target: BetaBrowserRefTarget
    """
    An element on the page, identified by a reference from a prior `read_page` or
    `find` result. References are scoped to the tab that produced them and become
    stale after navigation or a major re-render.
    """

    value: BetaBrowserFormInputValue
    """The value to set."""

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
