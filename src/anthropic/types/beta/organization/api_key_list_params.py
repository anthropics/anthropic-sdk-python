# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, TypedDict

__all__ = ["APIKeyListParams"]


class APIKeyListParams(TypedDict, total=False):
    after_id: str
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately after this object.
    """

    before_id: str
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately before this object.
    """

    created_by_user_id: Optional[str]
    """Filter by the ID of the User who created the object."""

    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.
    """

    status: Optional[Literal["active", "archived", "expired", "inactive"]]
    """Filter by API key status."""

    workspace_id: Optional[str]
    """Filter by Workspace ID."""
