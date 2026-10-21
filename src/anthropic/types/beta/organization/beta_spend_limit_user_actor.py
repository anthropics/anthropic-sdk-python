from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitUserActor"]


class BetaSpendLimitUserActor(BaseModel):
    """A user within the organization.

    `name` and `email_address` are
    null when the underlying account is unavailable or has been deleted;
    `deleted` is true only for deleted accounts.
    """

    deleted: bool
    """True only when the underlying account has been deleted."""

    email_address: Optional[str] = None
    """The user's email address.

    Null when the account is unavailable or has been deleted.
    """

    name: Optional[str] = None
    """The user's current display name.

    Null when the account is unavailable, has been deleted, or has no name set.
    """

    type: Literal["user_actor"]
    """Actor type. Always `user_actor`."""

    user_id: str
    """Tagged ID of the user."""
