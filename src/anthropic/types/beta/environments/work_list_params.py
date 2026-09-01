# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["WorkListParams"]


class WorkListParams(TypedDict, total=False):
    limit: int
    """Maximum number of work items to return"""

    page: Optional[str]
    """Opaque cursor from previous response for pagination"""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
