from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["VersionListParams"]


class VersionListParams(TypedDict, total=False):
    limit: Optional[int]
    """Number of results to return per page.

    Ranges from `1` to `1000`. Defaults to `20`.
    """

    page: Optional[str]
    """Optionally set to the `next_page` token from the previous response."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
