from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_mcp_oauth_update_params import BetaManagedAgentsMCPOAuthUpdateParams
from .beta_managed_agents_static_bearer_update_params import BetaManagedAgentsStaticBearerUpdateParams
from .beta_managed_agents_environment_variable_update_params import BetaManagedAgentsEnvironmentVariableUpdateParams

__all__ = ["CredentialUpdateParams", "Auth"]


class CredentialUpdateParams(TypedDict, total=False):
    vault_id: Required[str]
    """Identifier of the vault containing the credential."""

    auth: Auth
    """Updated authentication details for a credential."""

    display_name: Optional[str]
    """Updated human-readable name for the credential. 1-255 characters."""

    metadata: Optional[Dict[str, Optional[str]]]
    """Metadata patch.

    Set a key to a string to upsert it, or to null to delete it. Omitted keys are
    preserved.
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


Auth: TypeAlias = Union[
    BetaManagedAgentsMCPOAuthUpdateParams,
    BetaManagedAgentsStaticBearerUpdateParams,
    BetaManagedAgentsEnvironmentVariableUpdateParams,
]
