from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentArchivedRunError"]


class BetaManagedAgentsAgentArchivedRunError(BaseModel):
    """The deployment's agent was archived."""

    message: str
    """Human-readable error description."""

    type: Literal["agent_archived_error"]
