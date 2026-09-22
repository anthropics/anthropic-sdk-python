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
    """The maximum number of versions to return per page. Defaults to 20."""

    memory_id: str
    """Return only versions of the memory with this ID (`mem_...`).

    The filter still works after the memory is deleted. The results then include the
    version whose `operation` is `deleted`.
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
    """Selects which projection of a `memory` or `memory_version` the server returns.

    `basic` returns the object with `content` set to `null`; `full` populates
    `content`. When omitted, the default is endpoint-specific: retrieve operations
    default to `full`; list, create, and update operations default to `basic`.
    Listing with `view=full` caps `limit` at 20.
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
