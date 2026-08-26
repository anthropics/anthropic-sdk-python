# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._utils import PropertyInfo
from ...._models import BaseModel
from .beta_aws_external_key_config import BetaAWSExternalKeyConfig
from .beta_gcp_external_key_config import BetaGCPExternalKeyConfig
from .beta_azure_external_key_config import BetaAzureExternalKeyConfig
from .beta_external_key_attached_attachment import BetaExternalKeyAttachedAttachment
from .beta_external_key_unattached_attachment import BetaExternalKeyUnattachedAttachment

__all__ = ["BetaExternalKey", "Attachment", "ProviderConfig"]

Attachment: TypeAlias = Annotated[
    Union[BetaExternalKeyAttachedAttachment, BetaExternalKeyUnattachedAttachment], PropertyInfo(discriminator="type")
]

ProviderConfig: TypeAlias = Annotated[
    Union[BetaAWSExternalKeyConfig, BetaGCPExternalKeyConfig, BetaAzureExternalKeyConfig],
    PropertyInfo(discriminator="type"),
]


class BetaExternalKey(BaseModel):
    """CMEK external key config belonging to the caller's organization.

    Configs are organization-scoped. Workspaces attach to a config; once any
    workspace references it, the provider fields become effectively immutable
    (existing encrypted data needs the config for decrypt).
    """

    id: str
    """Identifier of the external key config.

    A tagged ID prefixed `ekey_`, or — for organizations on the Claude Platform on
    AWS — the AWS KMS key ARN.
    """

    attachment: Attachment
    """
    Whether any workspace uses this config to encrypt its data — counting live and
    archived workspaces (an archived workspace's data remains encrypted under the
    config), excluding deleted ones. Only an attached config is used by the
    encryption path; an `unattached` config is inert and can be deleted.
    """

    created_at: datetime

    display_name: Optional[str] = None
    """Human-friendly display name. Null if none was set."""

    geo: str
    """Data residency geo.

    Selects which regional validator handles this key's encrypt/decrypt roundtrips.
    """

    provider_config: ProviderConfig
    """KMS provider identity and auth coordinates."""

    type: Literal["external_key"]

    updated_at: datetime
