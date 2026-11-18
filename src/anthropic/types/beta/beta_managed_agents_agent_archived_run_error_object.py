from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentArchivedRunErrorObject"]


class BetaManagedAgentsAgentArchivedRunErrorObject(BaseModel):
    """The deployment's agent was archived."""

    message: str
    """Human-readable error description."""

    type: Literal["agent_archived_error"]
