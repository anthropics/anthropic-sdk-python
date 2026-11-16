from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsFileNotFoundRunErrorObject"]


class BetaManagedAgentsFileNotFoundRunErrorObject(BaseModel):
    """A file resource referenced by the deployment no longer exists."""

    message: str
    """Human-readable error description."""

    type: Literal["file_not_found_error"]
