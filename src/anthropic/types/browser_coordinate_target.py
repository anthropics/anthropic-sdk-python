from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["BrowserCoordinateTarget"]


class BrowserCoordinateTarget(BaseModel):
    """
    A point in the browser viewport, in viewport pixels (the same frame as a
    full-viewport screenshot).
    """

    type: Literal["coordinate"]

    x: int
    """Pixels from the left edge of the viewport."""

    y: int
    """Pixels from the top edge of the viewport."""
