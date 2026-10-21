from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAnthropicSkill"]


class BetaManagedAgentsAnthropicSkill(BaseModel):
    """A resolved Anthropic-managed skill."""

    skill_id: str

    type: Literal["anthropic"]

    version: str
