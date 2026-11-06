from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView

__all__ = ["MemoryListParams"]


class MemoryListParams(TypedDict, total=False):
    depth: int
    """How far below `path_prefix` to list.

    Defaults to `0`, which lists every memory below the prefix.

    Pass `1` to list only the direct children. Deeper memories are then grouped into
    `memory_prefix` items.
    """

    limit: int
    """The maximum number of items to return per page, from 1 to 100. Defaults to 20.

    With `view=full`, a page holds at most 20 items. `memory` and `memory_prefix`
    items both count toward the limit.
    """

    page: str
    """The `next_page` value from a previous response, to get the next page.

    Omit it to get the first page.
    """

    path_prefix: str
    """Return only memories whose path starts with this prefix, such as `/notes/`.

    This value appears in request URLs. Do not include secrets or personally
    identifiable information.

    Omit it to list the whole store. The prefix must end with `/` and matches whole
    segments, so `/notes/` matches `/notes/todo.md` but not
    `/notes-archive/todo.md`.
    """

    view: BetaManagedAgentsMemoryView
    """Whether each memory in the response includes `content`.

    Defaults to `basic`, which sets it to `null`.

    With `full`, a page holds at most 20 items.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
    `managed-agents-2026-04-01` in this header.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
