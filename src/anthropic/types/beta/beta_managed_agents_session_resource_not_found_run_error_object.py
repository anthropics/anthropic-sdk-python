from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSessionResourceNotFoundRunErrorObject"]


class BetaManagedAgentsSessionResourceNotFoundRunErrorObject(BaseModel):
    """A referenced resource no longer exists and its kind was not reported."""

    message: str
    """Human-readable error description."""

    type: Literal["session_resource_not_found_error"]
