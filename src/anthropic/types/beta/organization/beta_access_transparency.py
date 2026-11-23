from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAccessTransparency"]


class BetaAccessTransparency(BaseModel):
    """Whether Access Transparency is on. Read-only."""

    type: Literal["disabled", "enabled"]
