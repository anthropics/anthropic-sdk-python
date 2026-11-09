from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from .user_profile_list_order import UserProfileListOrder
from .user_profile_list_order_by import UserProfileListOrderBy
from .user_profile_enforcement_status import UserProfileEnforcementStatus

__all__ = ["UserProfileListParams"]


class UserProfileListParams(TypedDict, total=False):
    enforcement_status: List[UserProfileEnforcementStatus]
    """
    Return only the user profiles whose `enforcement_status` is one of these values:
    `unrestricted`, `pending`, `restricted` or `banned`. Repeat the parameter to
    match any of several. With it set, a page may hold fewer than `limit` profiles,
    or none, and still carry a `next_page`: the service examines a bounded number of
    profiles per request, and only a null `next_page` means the listing is complete.
    Rejected with `invalid_request_error` under the `user-profiles-2026-09-04` and
    earlier beta headers. Fails with `overloaded_error` when a profile's enforcement
    actions cannot be read for the moment.
    """

    limit: int
    """The maximum number of user profiles to return, from 1 to 100. Defaults to 20."""

    order: UserProfileListOrder
    """The sort direction, applied to the field that `order_by` selects.

    Defaults to `desc`.
    """

    order_by: UserProfileListOrderBy
    """The field to sort user profiles by, in the direction that `order` sets.

    Defaults to `created_at`.
    """

    page: str
    """
    The cursor for the page to return, taken from `next_page` in a previous
    response.

    Leave it out to get the first page.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
