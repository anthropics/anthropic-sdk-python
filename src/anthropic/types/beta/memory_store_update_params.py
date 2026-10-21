from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryStoreUpdateParams"]


class MemoryStoreUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """New description for the store, up to 1,024 characters.

    Pass an empty string to clear it.
    """

    metadata: Optional[Dict[str, Optional[str]]]
    """Changes to apply to the memory store's metadata.

    Keys you leave out keep their values.

    Set a key to a string to add or replace it, or to `null` to remove it. After the
    change, the metadata can hold at most 16 key-value pairs. Keys are 1 to 64
    characters long and values at most 512 characters.
    """

    name: Optional[str]
    """
    The new name of the memory store, 1 to 255 characters long, without control
    characters.

    Sessions created after the change use the new name for the store's directory
    under `/mnt/memory/`.
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
