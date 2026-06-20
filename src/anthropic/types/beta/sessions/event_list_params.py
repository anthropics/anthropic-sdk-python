# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, Annotated, TypedDict

from ...._types import SequenceNotStr
from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    created_at_gt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gt]", format="iso8601")]
    """Return events created after this time (exclusive)."""

    created_at_gte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gte]", format="iso8601")]
    """Return events created at or after this time (inclusive)."""

    created_at_lt: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lt]", format="iso8601")]
    """Return events created before this time (exclusive)."""

    created_at_lte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lte]", format="iso8601")]
    """Return events created at or before this time (inclusive)."""

    limit: int
    """Query parameter for limit"""

    order: Literal["asc", "desc"]
    """Sort direction for results, ordered by created_at.

    Defaults to asc (chronological).
    """

    page: str
    """Opaque pagination cursor from a previous response's next_page."""

    types: SequenceNotStr[str]
    """Filter by event type.

    Values match the `type` field on returned events (for example, `user.message` or
    `agent.tool_use`). Omit to return all event types.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
