from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentThinkingPreview"]


class BetaManagedAgentsAgentThinkingPreview(BaseModel):
    id: str
    """The id the buffered agent.thinking will carry if it is emitted.

    Start-only — no event_delta events follow.
    """

    type: Literal["agent.thinking"]
