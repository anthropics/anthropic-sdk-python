# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .beta_aws_external_key_config_param import BetaAWSExternalKeyConfigParam
from .beta_gcp_external_key_config_param import BetaGCPExternalKeyConfigParam
from .beta_azure_external_key_config_param import BetaAzureExternalKeyConfigParam

__all__ = ["ExternalKeyCreateParams", "ProviderConfig"]


class ExternalKeyCreateParams(TypedDict, total=False):
    provider_config: Required[ProviderConfig]
    """KMS provider identity and auth coordinates."""

    display_name: Optional[str]
    """Human-friendly display name."""

    geo: Literal["us"]
    """Data residency geo. Only `us` is supported."""


ProviderConfig: TypeAlias = Union[
    BetaAWSExternalKeyConfigParam, BetaGCPExternalKeyConfigParam, BetaAzureExternalKeyConfigParam
]
