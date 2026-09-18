from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_memory_view import BetaManagedAgentsMemoryView

__all__ = ["MemoryVersionRetrieveParams"]


class MemoryVersionRetrieveParams(TypedDict, total=False):
    memory_store_id: Required[str]

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
