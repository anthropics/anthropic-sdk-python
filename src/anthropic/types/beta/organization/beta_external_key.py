from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_aws_external_key_config import BetaAWSExternalKeyConfig
from .beta_gcp_external_key_config import BetaGCPExternalKeyConfig
from .beta_azure_external_key_config import BetaAzureExternalKeyConfig
from .beta_external_key_attached_attachment import BetaExternalKeyAttachedAttachment
from .beta_external_key_unattached_attachment import BetaExternalKeyUnattachedAttachment

__all__ = ["BetaExternalKey", "Attachment", "ProviderConfig"]

Attachment: TypeAlias = Annotated[
    Union[BetaExternalKeyAttachedAttachment, BetaExternalKeyUnattachedAttachment], UnionDiscriminator("type")
]

ProviderConfig: TypeAlias = Annotated[
    Union[BetaAWSExternalKeyConfig, BetaGCPExternalKeyConfig, BetaAzureExternalKeyConfig], UnionDiscriminator("type")
]


class BetaExternalKey(BaseModel):
    """CMEK external key config belonging to the caller's organization.

    Configs are organization-scoped. Workspaces attach to a config; once any
    workspace references it, the provider fields become effectively immutable
    (existing encrypted data needs the config for decrypt).
    """

    id: str
    """
    Identifier of the external key config: a tagged ID prefixed `ekey_`, or, on
    Claude Platform on AWS, an AWS KMS key's ARN.
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
    """Data residency geo. Selects the region this key is used in."""

    provider_config: ProviderConfig
    """KMS provider identity and auth coordinates."""

    type: Literal["external_key"]

    updated_at: datetime

    user_profile_id: Optional[str] = None
    """
    ID of the user profile the key is bound to, or null if the key is not bound to
    one. A key bound to a user profile can only be attached to a Workspace that has
    the same user profile. A key that isn't bound can be attached to a Workspace
    whatever its user profile.
    """
