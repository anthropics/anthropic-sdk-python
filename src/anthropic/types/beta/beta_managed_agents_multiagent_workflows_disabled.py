from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsMultiagentWorkflowsDisabled"]


class BetaManagedAgentsMultiagentWorkflowsDisabled(BaseModel):
    """The agent cannot start workflow runs."""

    type: Literal["disabled"]
