from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginOwnerUser"]


class BetaPluginOwnerUser(BaseModel):
    type: Literal["user"]
    """The Plugin lives in one member's personal plugin marketplace."""

    user_id: str
    """The member's User ID."""
