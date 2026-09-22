from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

from ..anthropic_beta_param import AnthropicBetaParam
from .beta_cloud_config_params import BetaCloudConfigParams
from .beta_self_hosted_config_params import BetaSelfHostedConfigParams

__all__ = ["EnvironmentUpdateParams", "Config"]


class EnvironmentUpdateParams(TypedDict, total=False):
    config: Optional[Config]
    """Updated environment configuration"""

    description: Optional[str]
    """Updated description of the environment.

    Omit to preserve; null clears to null; an empty string is stored as an empty
    string.
    """

    metadata: Dict[str, Optional[str]]
    """User-provided metadata key-value pairs.

    Set a value to null or empty string to delete the key.
    """

    name: Optional[str]
    """Updated name for the environment"""

    scope: Optional[Literal["organization", "account"]]
    """The visibility scope for this environment.

    'organization' makes the environment visible to all accounts. 'account'
    restricts visibility to the owning account only.
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
