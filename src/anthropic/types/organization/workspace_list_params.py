from __future__ import annotations

from typing_extensions import TypedDict

from ..._types import SequenceNotStr

__all__ = ["WorkspaceListParams"]


class WorkspaceListParams(TypedDict, total=False):
    after_id: str
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately after this object.
    """

    before_id: str
    """ID of the object to use as a cursor for pagination.

    When provided, returns the page of results immediately before this object.
    """

    ids: SequenceNotStr[str]
    """Only the Workspaces with these IDs, at most 100.

    `include_archived` and `include_default` still apply, and IDs of Workspaces the
    caller can't list are left out.
    """

    include_archived: bool
    """Whether to include Workspaces that have been archived in the response"""

    include_default: bool
    """Whether to include the organization's default Workspace in the response"""

    limit: int
    """Number of items to return per page.

    Defaults to `20`. Ranges from `1` to `1000`.
    """
