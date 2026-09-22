from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["UserProfileListParams"]


class UserProfileListParams(TypedDict, total=False):
    limit: int
    """The maximum number of user profiles to return, from 1 to 100. Defaults to 20."""

    order: Literal["asc", "desc"]
    """The sort direction, applied to the field that `order_by` selects.

    Defaults to `desc`.

    - `asc` - Oldest first when `order_by` is `created_at`, or names in ascending
      order when `order_by` is `name`.
    - `desc` - Newest first when `order_by` is `created_at`, or names in descending
      order when `order_by` is `name`. This is the default.
    """

    order_by: Literal["created_at", "name"]
    """The field to sort user profiles by, in the direction that `order` sets.

    Defaults to `created_at`.

    - `created_at` - Sort by when each user profile was created. This is the
      default.
    - `name` - Sort by `name`, ignoring the case of ASCII letters. Profiles without
      a name come last in either direction.
    """

    page: str
    """
    The cursor for the page to return, taken from `next_page` in a previous
    response.

    Leave it out to get the first page.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
