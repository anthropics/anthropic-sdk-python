from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentReference"]


class BetaManagedAgentsAgentReference(BaseModel):
    """A resolved agent reference with a concrete version."""

    id: str

    type: Literal["agent"]

    version: int
