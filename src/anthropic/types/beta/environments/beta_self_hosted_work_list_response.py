# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...._models import BaseModel
from .beta_self_hosted_work import BetaSelfHostedWork

__all__ = ["BetaSelfHostedWorkListResponse"]


class BetaSelfHostedWorkListResponse(BaseModel):
    """Response when listing work items with cursor-based pagination."""

    data: List[BetaSelfHostedWork]
    """List of work items"""

    next_page: Optional[str] = None
    """Opaque cursor for fetching the next page of results"""
