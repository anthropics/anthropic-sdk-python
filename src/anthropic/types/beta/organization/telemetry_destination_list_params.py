from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ...._types import SequenceNotStr
from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["TelemetryDestinationListParams"]


class TelemetryDestinationListParams(TypedDict, total=False):
    limit: int
    """Number of destinations to return per page, between 1 and 1,000. Defaults to 20."""

    page: str
    """Opaque cursor from a previous response's `next_page`.

    Leave it out to get the first page.
    """

    workspace_ids: SequenceNotStr[str]
    """
    Return only the destinations that cover at least one of these workspaces
    (`wrkspc_...`).

    Send at most 100 IDs, as `workspace_ids[]`. A destination covers a workspace
    when its `workspaces.type` is `all`, when its `include` list has the workspace,
    or when its `exclude` list doesn't have it. Destinations in either state can
    match. An ID that isn't the ID of one of the organization's workspaces doesn't
    match any destination, not even one whose type is `all`.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `telemetry-destinations-2026-08-11`
    in this header.
    """
