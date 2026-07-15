# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, Annotated, TypedDict

from ...._utils import PropertyInfo
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
    `..` segments, control or format characters, and must be NFC-normalized. Paths
    are case-sensitive.
    """

    view: BetaManagedAgentsMemoryView
    """Query parameter for view"""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
