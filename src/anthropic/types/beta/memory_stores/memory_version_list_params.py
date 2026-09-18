from __future__ import annotations

from typing import List, Union
from datetime import datetime
from typing_extensions import Annotated, TypedDict

from ...._utils import PropertyInfo
from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView
from .beta_managed_agents_memory_version_operation import BetaManagedAgentsMemoryVersionOperation

__all__ = ["MemoryVersionListParams"]


class MemoryVersionListParams(TypedDict, total=False):
    api_key_id: str

    created_at_gte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[gte]", format="iso8601")]
    """Return versions created at or after this time (inclusive)."""

    created_at_lte: Annotated[Union[str, datetime], PropertyInfo(alias="created_at[lte]", format="iso8601")]
    """Return versions created at or before this time (inclusive)."""

    limit: int

    memory_id: str

    operation: BetaManagedAgentsMemoryVersionOperation
    """The kind of mutation a `memory_version` records.

    Every non-no-op mutation to a memory appends exactly one version row with one of
    these values.
    """

    page: str

    service_account_id: str

    session_id: str

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
