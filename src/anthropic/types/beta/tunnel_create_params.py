# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["TunnelCreateParams"]


class TunnelCreateParams(TypedDict, total=False):
    display_name: Optional[str]
    """Optional human-readable name for the tunnel (1-255 characters)."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
