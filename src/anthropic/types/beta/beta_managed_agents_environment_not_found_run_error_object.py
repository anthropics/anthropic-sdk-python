from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsEnvironmentNotFoundRunErrorObject"]


class BetaManagedAgentsEnvironmentNotFoundRunErrorObject(BaseModel):
    """The deployment's environment no longer exists."""

    message: str
    """Human-readable error description."""

    type: Literal["environment_not_found_error"]
