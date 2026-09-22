from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView
from .beta_managed_agents_precondition_param import BetaManagedAgentsPreconditionParam

__all__ = ["MemoryUpdateParams"]


class MemoryUpdateParams(TypedDict, total=False):
    memory_store_id: Required[str]
    """The ID of the memory store that holds the memory (`memstore_...`)."""

    view: BetaManagedAgentsMemoryView
    """Selects which projection of a `memory` or `memory_version` the server returns.

    `basic` returns the object with `content` set to `null`; `full` populates
    `content`. When omitted, the default is endpoint-specific: retrieve operations
    default to `full`; list, create, and update operations default to `basic`.
    Listing with `view=full` caps `limit` at 20.
    """

    content: Optional[str]
    """New UTF-8 text content for the memory.

    Maximum 100 kB (102,400 bytes). Omit to leave the content unchanged (e.g., for a
    rename-only update).
    """

    path: Optional[str]
    """New path for the memory (a rename).

    Must start with `/`, contain at least one non-empty segment, and be at most
    1,024 bytes. Must not contain empty segments, `.` or `..` segments, control or
    format characters, or the Unicode line and paragraph separators (U+2028,
    U+2029), and must be NFC-normalized. Paths are case-sensitive. The memory's `id`
    is preserved across renames. Omit to leave the path unchanged.
    """

    precondition: BetaManagedAgentsPreconditionParam
    """
    Optimistic-concurrency precondition: the update applies only if the memory's
    stored `content_sha256` equals the supplied value. On mismatch, the request
    returns `memory_precondition_failed_error` (HTTP 409); re-read the memory and
    retry against the fresh state. If the precondition fails but the stored state
    already exactly matches the requested `content` and `path`, the server returns
    200 instead of 409.
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
