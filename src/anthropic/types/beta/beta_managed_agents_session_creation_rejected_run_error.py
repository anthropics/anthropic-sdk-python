from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsSessionCreationRejectedRunError"]


class BetaManagedAgentsSessionCreationRejectedRunError(BaseModel):
    """The session create request was rejected with a non-retryable validation error."""

    message: str
    """Human-readable error description."""

    type: Literal["session_creation_rejected_error"]
