from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsFileNotFoundDeploymentPausedReasonErrorObject"]


class BetaManagedAgentsFileNotFoundDeploymentPausedReasonErrorObject(BaseModel):
    """A file resource referenced by the deployment no longer exists."""

    type: Literal["file_not_found_error"]
