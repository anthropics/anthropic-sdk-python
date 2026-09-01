# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["RuleListParams"]


class RuleListParams(TypedDict, total=False):
    include_archived: bool
    """Include archived resources. Defaults to false."""

    issuer_id: Optional[str]
    """Filter to rules referencing this federation issuer."""

    limit: int
    """Number of results per page."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
