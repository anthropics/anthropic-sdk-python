from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryStoreUpdateParams"]


class MemoryStoreUpdateParams(TypedDict, total=False):
    description: Optional[str]
    """New description for the store, up to 1024 characters.

    Pass an empty string to clear it.
    """

    metadata: Optional[Dict[str, Optional[str]]]
    """Metadata patch.

    Set a key to a string to upsert it, or to null to delete it. Omit the field to
    preserve. The stored bag is limited to 16 keys (up to 64 chars each) with values
    up to 512 chars.
    """

    name: Optional[str]
    """New human-readable name for the store.

    1–255 characters; no control characters. Renaming changes the slug used for the
    store's `mount_path` in sessions created after the update.
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
