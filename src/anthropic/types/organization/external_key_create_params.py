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

    user_profile_id: Optional[str]
    """ID of a user profile to bind the key to.

    A user profile represents one of your customers: bind a customer's key to that
    customer's user profile. A key bound to a user profile can only be attached to a
    Workspace that has the same user profile, and the binding cannot be changed
    later. Omit this field only for your organization's own key, because a key
    created without a user profile ID can be attached to any Workspace, including
    another customer's.
    """


ProviderConfig: TypeAlias = Union[AWSExternalKeyConfigParam, GCPExternalKeyConfigParam, AzureExternalKeyConfigParam]
