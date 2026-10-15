from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaManagedAgentsUserActor"]


class BetaManagedAgentsUserActor(BaseModel):
    """A human user, for example acting through the Anthropic Console."""

    type: Literal["user_actor"]

    user_id: str
    """ID of the user (a `user_...` value)."""
