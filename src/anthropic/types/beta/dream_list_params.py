# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo
from .beta_dream_status import BetaDreamStatus
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["DreamListParams"]


class DreamListParams(TypedDict, total=False):
    created_at_gt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gt]", format="iso8601")]
    """
    Return dreams with `created_at` strictly after this timestamp (exclusive lower
    bound, RFC 3339). Unset applies no lower bound.
    """

    created_at_lt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lt]", format="iso8601")]
    """
    Return dreams with `created_at` strictly before this timestamp (exclusive upper
    bound, RFC 3339). Unset applies no upper bound.
    """

    include_archived: bool
    """Query parameter for include_archived"""

    limit: int
    """Query parameter for limit"""

    page: str
    """Query parameter for page"""

    statuses: List[BetaDreamStatus]
    """Filter by lifecycle status.

    Repeat the parameter to match any of multiple statuses. Empty applies no status
    filter.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
