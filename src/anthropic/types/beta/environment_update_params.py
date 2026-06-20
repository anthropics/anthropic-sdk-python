# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias, TypedDict

from ..._utils import PropertyInfo
from ..anthropic_beta_param import AnthropicBetaParam
from .beta_cloud_config_params import BetaCloudConfigParams
from .beta_self_hosted_config_params import BetaSelfHostedConfigParams

__all__ = ["EnvironmentUpdateParams", "Config"]


class EnvironmentUpdateParams(TypedDict, total=False):
    config: Optional[Config]
    """Updated environment configuration"""

    description: Optional[str]
    """Updated description of the environment"""

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

    betas: Annotated[List[AnthropicBetaParam], PropertyInfo(alias="anthropic-beta")]
    """Optional header to specify the beta version(s) you want to use."""


Config: TypeAlias = Union[BetaCloudConfigParams, BetaSelfHostedConfigParams]
