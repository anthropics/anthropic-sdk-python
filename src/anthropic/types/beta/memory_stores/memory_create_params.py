from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView

__all__ = ["MemoryCreateParams"]


class MemoryCreateParams(TypedDict, total=False):
    content: Required[Optional[str]]
    """The UTF-8 text content of the new memory. Pass `""` to create an empty memory.

    The maximum size is 100 kB (102,400 bytes).
    """

    path: Required[str]
    """The path of the new memory, such as `/projects/foo/notes.md`.

    Paths are case-sensitive.

    A path starts with `/` and has 1 to 20 segments. A segment can't be empty and
    can't be `.` or `..`. A path can't contain control characters, format
    characters, or the line and paragraph separators U+2028 and U+2029. It must be
    in Unicode Normalization Form C and at most 1,024 bytes long.
    """

    view: BetaManagedAgentsMemoryView
    """Whether a `memory` or `memory_version` in the response includes its `content`.

    Defaults to `full` on retrieve operations and to `basic` on list, create, and
    update operations.

    With `full`, list operations return at most 20 items per page.
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
