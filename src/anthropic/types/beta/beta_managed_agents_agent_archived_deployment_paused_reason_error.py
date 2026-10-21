from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAgentArchivedDeploymentPausedReasonError"]


class BetaManagedAgentsAgentArchivedDeploymentPausedReasonError(BaseModel):
    """The deployment's agent was archived."""

    type: Literal["agent_archived_error"]
