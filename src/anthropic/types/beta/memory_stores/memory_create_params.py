from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView

__all__ = ["MemoryCreateParams"]


class MemoryCreateParams(TypedDict, total=False):
    content: Required[Optional[str]]
    """UTF-8 text content for the new memory.

    Maximum 100 kB (102,400 bytes). Required; pass `""` explicitly to create an
    empty memory.
    """

    path: Required[str]
    """Hierarchical path for the new memory, e.g.

    `/projects/foo/notes.md`. Must start with `/`, contain at least one non-empty
    segment, and be at most 1,024 bytes. Must not contain empty segments, `.` or
    `..` segments, control or format characters, or the Unicode line and paragraph
    separators (U+2028, U+2029), and must be NFC-normalized. Paths are
    case-sensitive.
    """

    view: BetaManagedAgentsMemoryView
    """Selects which projection of a `memory` or `memory_version` the server returns.

    `basic` returns the object with `content` set to `null`; `full` populates
    `content`. When omitted, the default is endpoint-specific: retrieve operations
    default to `full`; list, create, and update operations default to `basic`.
    Listing with `view=full` caps `limit` at 20.
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
