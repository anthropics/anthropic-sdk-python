from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ..anthropic_beta_param import AnthropicBetaParam

__all__ = ["VaultListParams"]


class VaultListParams(TypedDict, total=False):
    include_archived: bool
    """Whether to include archived vaults in the results. Defaults to `false`."""

    limit: int
    """Maximum number of vaults to return per page. Defaults to 20, maximum 100."""

    page: str
    """
    The `next_page` value from a previous
    [List Vaults](https://platform.claude.com/docs/en/api/beta/vaults/list)
    response, to get the next page. Leave it out to get the first page.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send `managed-agents-2026-04-01` in this
    header.
    """

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
