from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["WorkspaceListParams"]


class WorkspaceListParams(TypedDict, total=False):
    limit: int
    """Number of entries to return per page, between 1 and 1,000. Defaults to 20."""

    page: str
    """Opaque cursor from a previous response's `next_page`.

    Leave it out to get the first page.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
    in this header.
    """
