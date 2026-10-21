from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaEnvironmentDeleteResponse"]


class BetaEnvironmentDeleteResponse(BaseModel):
    """Response after deleting an environment."""

    id: str
    """Environment identifier"""

    type: Literal["environment_deleted"]
    """The type of response"""
