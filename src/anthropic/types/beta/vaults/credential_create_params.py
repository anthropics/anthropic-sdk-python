from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_managed_agents_mcp_oauth_create_params import BetaManagedAgentsMCPOAuthCreateParams
from .beta_managed_agents_static_bearer_create_params import BetaManagedAgentsStaticBearerCreateParams
from .beta_managed_agents_environment_variable_create_params import BetaManagedAgentsEnvironmentVariableCreateParams

__all__ = ["CredentialCreateParams", "Auth"]


class CredentialCreateParams(TypedDict, total=False):
    auth: Required[Auth]
    """Authentication details for creating a credential."""

    display_name: Optional[str]
    """Human-readable name for the credential. Up to 255 characters."""

    metadata: Dict[str, str]
    """Arbitrary key-value metadata to attach to the credential.

    Maximum 16 pairs, keys up to 64 chars, values up to 512 chars.
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
    BetaManagedAgentsMCPOAuthCreateParams,
    BetaManagedAgentsStaticBearerCreateParams,
    BetaManagedAgentsEnvironmentVariableCreateParams,
]
