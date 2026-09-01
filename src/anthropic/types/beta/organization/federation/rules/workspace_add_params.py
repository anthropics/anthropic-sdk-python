# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from .....anthropic_beta_param import AnthropicBetaParam

__all__ = ["WorkspaceAddParams"]


class WorkspaceAddParams(TypedDict, total=False):
    workspace_id: Required[str]
    """Tagged ID of the workspace to enable this rule for."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""
