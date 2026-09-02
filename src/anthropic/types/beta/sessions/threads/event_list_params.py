# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    session_id: Required[str]

    limit: int
    """Query parameter for limit"""

    page: str
    """Query parameter for page"""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
