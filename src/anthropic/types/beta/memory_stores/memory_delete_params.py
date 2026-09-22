from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryDeleteParams"]


class MemoryDeleteParams(TypedDict, total=False):
    memory_store_id: Required[str]
    """The ID of the memory store that holds the memory (`memstore_...`)."""

    expected_content_sha256: str
    """
    Delete the memory only if its current `content_sha256` equals this value, given
    as 64 lowercase hexadecimal characters. Omit it to delete unconditionally.

    If the hashes differ, the request fails with HTTP status 409 and nothing is
    deleted.
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
