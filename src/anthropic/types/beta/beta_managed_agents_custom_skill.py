from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsCustomSkill"]


class BetaManagedAgentsCustomSkill(BaseModel):
    """A resolved user-created custom skill."""

    skill_id: str

    type: Literal["custom"]

    version: str
