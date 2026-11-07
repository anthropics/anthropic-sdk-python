from typing import Optional

from ..._models import BaseModel

__all__ = ["BetaComputerLeftClickDragConfig"]


class BetaComputerLeftClickDragConfig(BaseModel):
    """``left_click_drag``'s config overrides."""

    defer_loading: Optional[bool] = None
    """Defer loading for this member.

    Must resolve to the same value on every enabled member of the toolset.
    """

    enabled: Optional[bool] = None
    """Whether this member is offered to the model.

    Default is per member, per the toolset's documentation. A member whose enabled
    resolves false is withheld from the served schema.
    """
