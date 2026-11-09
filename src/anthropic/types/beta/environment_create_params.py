from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_cloud_config_params import BetaCloudConfigParams
from .beta_self_hosted_config_params import BetaSelfHostedConfigParams

__all__ = ["EnvironmentCreateParams", "Config"]


class EnvironmentCreateParams(TypedDict, total=False):
    name: Required[str]
    """Human-readable name for the environment"""

    config: Optional[Config]
    """Environment configuration"""

    description: Optional[str]
    """Optional description of the environment"""

    metadata: Dict[str, str]
    """User-provided metadata key-value pairs"""

    scope: Optional[Literal["organization", "account"]]
    """The visibility scope for this environment.

    'organization' makes the environment visible to all accounts. 'account'
    restricts visibility to the owning account only. API organizations support only
    'organization'; 'account' is rejected. If not specified, defaults based on
    organization type.
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


Config: TypeAlias = Union[BetaCloudConfigParams, BetaSelfHostedConfigParams]
