from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ...._types import SequenceNotStr

__all__ = ["BetaTelemetryDestinationWorkspacesIncludeParams"]


class BetaTelemetryDestinationWorkspacesIncludeParams(TypedDict, total=False):
    """Cover only the workspaces on the list."""

    type: Required[Literal["include"]]

    workspace_ids: SequenceNotStr[str]
    """The IDs of the workspaces on the destination's list (`wrkspc_...`).

    At most 100 per request.

    On create, these workspaces become the destination's list. If you leave
    `workspace_ids` out, the list starts empty. If the API refuses one of the IDs,
    it doesn't create the destination.

    On update, `workspace_ids` replaces the whole list. A workspace that stays on
    the list keeps its entry and its `created_at`. An empty array empties the list.
    If you leave `workspace_ids` out and the type stays the same, the list doesn't
    change. If you leave it out and the type changes, the new list starts empty.
    After a change to `include` without `workspace_ids`, the destination doesn't
    cover any workspace until one is added. After a change to `exclude` without
    `workspace_ids`, it covers every workspace.

    An ID sent more than once is added once. An archived workspace can't be added to
    a list. An update can keep an archived workspace that is already on the list.
    """
