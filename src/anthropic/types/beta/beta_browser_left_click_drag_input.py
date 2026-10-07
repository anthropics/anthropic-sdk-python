from typing import Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .beta_browser_coordinate_target import BetaBrowserCoordinateTarget

__all__ = ["BetaBrowserLeftClickDragInput"]


class BetaBrowserLeftClickDragInput(BaseModel):
    """Press at `from`, drag to `target`, release. Both must be coordinate targets."""

    from_: BetaBrowserCoordinateTarget = FieldInfo(alias="from")
    """
    A point in the browser viewport, in viewport pixels (the same frame as a
    full-viewport screenshot).
    """

    target: BetaBrowserCoordinateTarget
    """
    A point in the browser viewport, in viewport pixels (the same frame as a
    full-viewport screenshot).
    """

    tab_id: Optional[str] = None
    """Tab to act on. Defaults to the active tab when omitted."""
