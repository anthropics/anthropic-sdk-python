# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

from ...._types import SequenceNotStr

__all__ = ["InviteListParams"]


class InviteListParams(TypedDict, total=False):
    after_id: str
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately after this object.
    """

    before_id: str
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately before this object.
    """

    email: str
    """Filter by the email address the Invite was sent to.

    Matches the same way as the Users list's `email` filter (normalized,
    case-insensitive).
    """

    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.
    """

    roles: SequenceNotStr[str]
    """Filter to items whose `role` equals one of the supplied values.

    Repeatable; values are OR'ed together.

    Accepted values depend on the organization type: Console and API organizations
    accept `user`, `developer`, `billing`, `admin`, and `claude_code_user`; Claude
    Enterprise organizations accept `user`, `owner`, `primary_owner`,
    `membership_admin`, and `managed`.
    """

    statuses: List[Literal["accepted", "expired", "pending"]]
    """Filter by Invite status.

    Repeatable; values are OR'ed together. Omit to return `pending`, `accepted`, and
    `expired` Invites alike.
    """
