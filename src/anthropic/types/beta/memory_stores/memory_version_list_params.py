from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView
from .beta_managed_agents_memory_version_operation import BetaManagedAgentsMemoryVersionOperation

__all__ = ["MemoryVersionListParams"]


class MemoryVersionListParams(TypedDict, total=False):
    api_key_id: str
    """Return only versions written with the API key that has this ID."""

    created_at_gte: Union[str, datetime]
    """Return versions created at or after this time (inclusive)."""

    created_at_lte: Union[str, datetime]
    """Return versions created at or before this time (inclusive)."""

    limit: int
    """The maximum number of versions to return per page, from 1 to 100.

    Defaults to 20.

    With `view=full`, a page holds at most 20 versions.
    """

    memory_id: str
    """Return only versions of the memory with this ID (`mem_...`).

    The filter still works after the memory is deleted. While that memory's versions
    are retained, the results include the version whose `operation` is `deleted`.
    """

    operation: BetaManagedAgentsMemoryVersionOperation
    """Return only versions that record this kind of change."""

    page: str
    """The `next_page` value from a previous response, to get the next page.

    Omit it to get the first page.
    """

    service_account_id: str
    """Return only versions written by the service account with this ID (`svac_...`)."""

    session_id: str
    """Return only versions written by the session with this ID."""

    view: BetaManagedAgentsMemoryView
    """Whether a `memory` or `memory_version` in the response includes its `content`.

    Defaults to `full` on retrieve operations and to `basic` on list, create, and
    update operations.

    With `full`, list operations return at most 20 items per page.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `agent-memory-2026-07-22` or
    `managed-agents-2026-04-01` in this header.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
