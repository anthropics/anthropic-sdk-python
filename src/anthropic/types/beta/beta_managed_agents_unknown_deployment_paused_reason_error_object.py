from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsUnknownDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsUnknownDeploymentPausedReasonErrorObject(BaseModel):
    """An unrecognized error auto-paused the deployment.

    A fallback variant; matches a run whose `error.type` is `unknown_error`.
    """

    type: Literal["unknown_error"]
