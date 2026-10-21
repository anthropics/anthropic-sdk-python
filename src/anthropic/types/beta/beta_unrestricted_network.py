from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaUnrestrictedNetwork"]


class BetaUnrestrictedNetwork(BaseModel):
    """Unrestricted network access."""

    type: Literal["unrestricted"]
    """Network policy type"""
