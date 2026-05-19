# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Required, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
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
    restricts visibility to the owning account only. Only applicable for self-hosted
    environments. If not specified, defaults based on organization type.
    """

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


Config: TypeAlias = Union[BetaCloudConfigParams, BetaSelfHostedConfigParams]
