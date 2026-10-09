from typing import Optional

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsWorkflowRunPhase"]


class BetaManagedAgentsWorkflowRunPhase(BaseModel):
    """A phase that a workflow run's plan declares."""

    id: str
    """Unique identifier for the phase."""

    description: Optional[str] = None
    """
    Description that the agent gave the phase, passed on as written, or `null` if it
    gave none.
    """

    name: str
    """Name that the agent gave the phase, passed on as written."""
