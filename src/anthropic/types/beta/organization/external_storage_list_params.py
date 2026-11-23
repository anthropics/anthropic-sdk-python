from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ...._types import SequenceNotStr
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["ExternalStorageListParams"]


class ExternalStorageListParams(TypedDict, total=False):
    limit: int
    """Number of results per page."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""

    user_profile_ids: Optional[SequenceNotStr[str]]
    """
    Returns only External Storage bound to one of these user profile IDs
    (`uprof_...`). An empty entry matches storage bound to no user profile. At most
    10 entries, counting repeats.
    """

    betas: List[AnthropicBetaParam]
    """This endpoint is in beta: requests must send `efs-2026-10-01` in this header."""
