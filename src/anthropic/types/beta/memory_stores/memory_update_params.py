# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView
from .beta_managed_agents_precondition_param import BetaManagedAgentsPreconditionParam

__all__ = ["MemoryUpdateParams"]


class MemoryUpdateParams(TypedDict, total=False):
    memory_store_id: Required[str]

    view: BetaManagedAgentsMemoryView
    """Query parameter for view"""

    content: Optional[str]
    """New UTF-8 text content for the memory.

    Maximum 100 kB (102,400 bytes). Omit to leave the content unchanged (e.g., for a
    rename-only update).
    """

    path: Optional[str]
    """New path for the memory (a rename).

    Must start with `/`, contain at least one non-empty segment, and be at most
    1,024 bytes. Must not contain empty segments, `.` or `..` segments, control or
    format characters, and must be NFC-normalized. Paths are case-sensitive. The
    memory's `id` is preserved across renames. Omit to leave the path unchanged.
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

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
