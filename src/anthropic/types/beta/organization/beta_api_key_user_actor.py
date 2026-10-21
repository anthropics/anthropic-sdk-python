from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAPIKeyUserActor"]


class BetaAPIKeyUserActor(BaseModel):
    type: Literal["user_actor"]
    """Principal type. Always `"user_actor"` for a User."""

    user_id: str
    """ID of the User the API key acts as."""
