from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentArchivedDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsAgentArchivedDeploymentPausedReasonErrorObject(BaseModel):
    """The deployment's agent was archived."""

    type: Literal["agent_archived_error"]
