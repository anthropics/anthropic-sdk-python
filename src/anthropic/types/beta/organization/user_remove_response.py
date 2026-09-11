from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["UserRemoveResponse"]


class UserRemoveResponse(BaseModel):
    id: str
    """ID of the User."""

    type: Literal["user_deleted"]
    """Deleted object type.

    For Users, this is always `"user_deleted"`.
    """
