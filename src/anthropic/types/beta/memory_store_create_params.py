from __future__ import annotations

from typing import Dict, List
from typing_extensions import Required, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["MemoryStoreCreateParams"]


class MemoryStoreCreateParams(TypedDict, total=False):
    name: Required[str]
    """
    The name of the memory store, 1 to 255 characters long, without control
    characters. Names don't have to be unique in a workspace.

    In a session, the store's directory under `/mnt/memory/` is based on this name.
    The name is lowercased and every run of characters other than ASCII letters and
    digits becomes one hyphen. The session's memory store resource gives the exact
    path in `mount_path`.

    See the
    [memory guide](https://platform.claude.com/docs/en/managed-agents/memory#how-the-agent-accesses-memory)
    to learn more about how agents access memory stores.
    """

    description: str
    """Free-text description of what the store contains, up to 1,024 characters.

    Included in the agent's system prompt when the store is attached, so word it to
    be useful to the agent.
    """

    metadata: Dict[str, str]
    """Key-value pairs for your own use, such as the end user that the store belongs
    to.

    The agent doesn't see them.

    A store has at most 16 pairs. Keys are 1 to 64 characters long and values at
    most 512 characters.
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
