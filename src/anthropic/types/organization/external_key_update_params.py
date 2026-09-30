from __future__ import annotations

from typing import Union, Optional
from typing_extensions import Literal, TypeAlias, TypedDict

from .aws_external_key_config_param import AWSExternalKeyConfigParam
from .gcp_external_key_config_param import GCPExternalKeyConfigParam
from .azure_external_key_config_param import AzureExternalKeyConfigParam

__all__ = ["ExternalKeyUpdateParams", "ProviderConfig"]


class ExternalKeyUpdateParams(TypedDict, total=False):
    display_name: Optional[str]
    """Human-friendly display name."""

    geo: Optional[Literal["us"]]
    """Data residency geo. Only `us` is supported."""

    provider_config: Optional[ProviderConfig]
    """KMS provider identity and auth coordinates."""


ProviderConfig: TypeAlias = Union[AWSExternalKeyConfigParam, GCPExternalKeyConfigParam, AzureExternalKeyConfigParam]
