# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryStoreCreateParams"]


class MemoryStoreCreateParams(TypedDict, total=False):
    name: Required[str]
    """Human-readable name for the store.

    Required; 1–255 characters; no control characters. The mount-path slug under
    `/mnt/memory/` is derived from this name (lowercased, non-alphanumeric runs
    collapsed to a hyphen). Names need not be unique within a workspace.
    """

    description: str
    """Free-text description of what the store contains, up to 1024 characters.

    Included in the agent's system prompt when the store is attached, so word it to
    be useful to the agent.
    """

    metadata: Dict[str, str]
    """
    Arbitrary key-value tags for your own bookkeeping (such as the end user a store
    belongs to). Up to 16 pairs; keys 1–64 characters; values up to 512 characters.
    Not visible to the agent.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""
