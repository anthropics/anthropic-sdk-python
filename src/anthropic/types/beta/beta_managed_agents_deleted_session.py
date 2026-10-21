from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsDeletedSession"]


class BetaManagedAgentsDeletedSession(BaseModel):
    """Confirmation that a `session` has been permanently deleted."""

    id: str

    type: Literal["session_deleted"]
