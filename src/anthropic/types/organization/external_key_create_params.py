from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .aws_external_key_config_param import AWSExternalKeyConfigParam
from .gcp_external_key_config_param import GCPExternalKeyConfigParam
from .azure_external_key_config_param import AzureExternalKeyConfigParam

__all__ = ["ExternalKeyCreateParams", "ProviderConfig"]


class ExternalKeyCreateParams(TypedDict, total=False):
    provider_config: Required[ProviderConfig]
    """KMS provider identity and auth coordinates."""

    display_name: Optional[str]
    """Human-friendly display name."""

    geo: Literal["us"]
    """Data residency geo. Only `us` is supported."""


ProviderConfig: TypeAlias = Union[AWSExternalKeyConfigParam, GCPExternalKeyConfigParam, AzureExternalKeyConfigParam]
