from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsReportUserActor"]


class BetaAnalyticsReportUserActor(BaseModel):
    deleted: bool
    """
    True when the account has been deleted, or when the user is no longer a member
    of the organization or its associated organizations (for example, their
    membership was removed or they were deprovisioned via your identity provider).
    `email_address` stays populated for removed users and is null when the account
    has been deleted. `name` follows the rules described on that field. The
    `user_id` is still populated for reconciliation.
    """

    email_address: Optional[str] = None
    """
    The user's current email address, including for users who are no longer members
    of the organization. Null when the account has been deleted and for
    system-minted service accounts.
    """

    name: Optional[str] = None
    """The user's current full name.

    Null when the user has not set one. `"Deleted User"` when the account has been
    deleted, or when the user is no longer a member and the organization hides
    removed users' names.
    """

    type: Literal["user_actor"]
    """Actor type. Always `"user_actor"`."""

    user_id: str
    """Tagged user ID."""
