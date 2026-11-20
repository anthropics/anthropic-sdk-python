from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Required, TypeAlias, TypedDict

from ...anthropic_beta_param import AnthropicBetaParam
from .beta_aws_external_storage_config_param import BetaAWSExternalStorageConfigParam
from .beta_gcp_external_storage_config_param import BetaGCPExternalStorageConfigParam

__all__ = ["ExternalStorageCreateParams", "ProviderConfig"]


class ExternalStorageCreateParams(TypedDict, total=False):
    provider_config: Required[ProviderConfig]

    display_name: Optional[str]
    """Human-friendly display name."""

    user_profile_id: Optional[str]
    """The user profile to bind the storage to.

    It can't be changed later. The storage can be attached only to Workspaces with
    this profile, and the bucket's setup must name the same ID.
    """

    betas: List[AnthropicBetaParam]
    """This endpoint is in beta: requests must send `efs-2026-10-01` in this header."""


ProviderConfig: TypeAlias = Union[BetaAWSExternalStorageConfigParam, BetaGCPExternalStorageConfigParam]
