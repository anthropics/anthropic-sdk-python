# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["VersionListParams"]


class VersionListParams(TypedDict, total=False):
    limit: int
    """Maximum results per page. Default 20, maximum 100."""

    page: str
    """Opaque pagination cursor."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
