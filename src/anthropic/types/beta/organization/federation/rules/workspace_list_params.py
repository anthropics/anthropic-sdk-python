# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Annotated, TypedDict

from ......_utils import PropertyInfo
from .....anthropic_beta_param import AnthropicBetaParam

__all__ = ["WorkspaceListParams"]


class WorkspaceListParams(TypedDict, total=False):
    limit: int
    """Number of results per page."""

    page: Optional[str]
    """Opaque cursor from a previous response's `next_page`."""

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
