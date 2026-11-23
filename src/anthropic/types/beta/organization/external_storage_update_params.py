from __future__ import annotations

from typing import List, Optional
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["ExternalStorageUpdateParams"]


class ExternalStorageUpdateParams(TypedDict, total=False):
    display_name: Required[Optional[str]]
    """Human-friendly display name; null clears it."""

    betas: List[AnthropicBetaParam]
    """This endpoint is in beta: requests must send `efs-2026-10-01` in this header."""
