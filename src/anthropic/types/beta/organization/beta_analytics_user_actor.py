from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsUserActor"]


class BetaAnalyticsUserActor(BaseModel):
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
    The user's email address, including for users who are no longer members of the
    organization or its associated organizations. Null when the account has been
    deleted (check `deleted`) and for system-minted service accounts, which have no
    person's mailbox behind them (check `name`).
    """

    name: Optional[str] = None
    """The user's full name.

    Null when the user has not set a name. Returns `"Deleted User"` when the account
    itself has been deleted, or when the user is no longer a member of the
    organization or its associated organizations and the organization has chosen to
    hide the names of removed users. Otherwise, the name stays populated for removed
    users. Rows for system-minted service accounts render the service name (for
    example, `"Claude Security"` for usage by Anthropic's security-patching service)
    or null.
    """

    type: Literal["user_actor"]
    """Actor type. Always `"user_actor"`."""

    user_id: str
    """Tagged user ID."""
