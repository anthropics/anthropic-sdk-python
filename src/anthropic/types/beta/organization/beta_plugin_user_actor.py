from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaPluginUserActor"]


class BetaPluginUserActor(BaseModel):
    email_address: Optional[str] = None
    """
    The member's email address; may be null, for example when they are no longer a
    member of the organization.
    """

    type: Literal["user_actor"]
    """A member of the organization."""

    user_id: str
    """The member's User ID."""
