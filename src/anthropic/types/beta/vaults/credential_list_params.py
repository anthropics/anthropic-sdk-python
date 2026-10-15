from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ...anthropic_beta_param import AnthropicBetaParam

__all__ = ["CredentialListParams"]


class CredentialListParams(TypedDict, total=False):
    include_archived: bool
    """Whether to include archived credentials in the results."""

    limit: int
    """Maximum number of credentials to return per page. Defaults to 20, maximum 100."""

    page: str
    """Opaque pagination token from a previous `list_credentials` response."""

    betas: List[AnthropicBetaParam]
    """Optional header to specify the beta version(s) you want to use."""

    workspace_id: str
    """Optional header to select the Workspace for this request.

    The value is a Workspace ID (for example, `wrkspc_011CZkZaBF1tNoB5wlCeusgy`).

    Only needed for credentials that can act on more than one Workspace. A
    credential that belongs to a specific Workspace may omit it; if sent, it must
    match that Workspace.
    """
