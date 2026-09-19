from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Literal, TypedDict

from ...._types import SequenceNotStr
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["EventListParams"]


class EventListParams(TypedDict, total=False):
    created_at_gt: Union[str, datetime]
    """Return events created after this time (exclusive).

    Compared against the event's `processed_at` value.
    """

    created_at_gte: Union[str, datetime]
    """Return events created at or after this time (inclusive).

    Compared against the event's `processed_at` value.
    """

    created_at_lt: Union[str, datetime]
    """Return events created before this time (exclusive).

    Compared against the event's `processed_at` value.
    """

    created_at_lte: Union[str, datetime]
    """Return events created at or before this time (inclusive).

    Compared against the event's `processed_at` value.
    """

    limit: int

    order: Literal["asc", "desc"]
    """Sort direction for results, ordered by the event's `processed_at`.

    Defaults to `asc` (chronological).
    """

    page: str
    """Opaque pagination cursor from a previous response's `next_page`."""

    types: SequenceNotStr[str]
    """Filter by event type.

    Values match the `type` field on returned events (for example, `user.message` or
    `agent.tool_use`). Omit to return all event types.
    """

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
