# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["WorkPollParams"]


class WorkPollParams(TypedDict, total=False):
    block_ms: Optional[int]
    """How long to wait for work to arrive before returning.

    Must be 1-999 in milliseconds. Defaults to non-blocking (returns immediately if
    no work is available).
    """

    reclaim_older_than_ms: Optional[int]
    """Reclaim unacknowledged work items older than this many milliseconds.

    If omitted, uses the default (5000ms).
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""

    anthropic_worker_id: Annotated[str, PropertyInfo(alias="Anthropic-Worker-ID")]
    """
    Unique identifier for the specific worker polling, used to track aggregated
    environment-level work metrics in Console
    """
