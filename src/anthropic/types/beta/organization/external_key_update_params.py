# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

from .beta_aws_external_key_config_param import BetaAWSExternalKeyConfigParam
from .beta_gcp_external_key_config_param import BetaGCPExternalKeyConfigParam
from .beta_azure_external_key_config_param import BetaAzureExternalKeyConfigParam

__all__ = ["ExternalKeyUpdateParams", "ProviderConfig"]


class ExternalKeyUpdateParams(TypedDict, total=False):
    display_name: Optional[str]
    """Human-friendly display name."""

    geo: Optional[Literal["us"]]
    """Data residency geo. Only `us` is supported."""

    provider_config: Optional[ProviderConfig]
    """KMS provider identity and auth coordinates."""


ProviderConfig: TypeAlias = Union[
    BetaAWSExternalKeyConfigParam, BetaGCPExternalKeyConfigParam, BetaAzureExternalKeyConfigParam
]
