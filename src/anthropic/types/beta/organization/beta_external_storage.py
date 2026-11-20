from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_aws_external_storage_config import BetaAWSExternalStorageConfig
from .beta_gcp_external_storage_config import BetaGCPExternalStorageConfig
from .beta_active_external_storage_status import BetaActiveExternalStorageStatus
from .beta_draining_external_storage_status import BetaDrainingExternalStorageStatus
from .beta_available_external_storage_status import BetaAvailableExternalStorageStatus
from .beta_pending_configuration_external_storage_status import BetaPendingConfigurationExternalStorageStatus

__all__ = ["BetaExternalStorage", "ProviderConfig", "Status"]

ProviderConfig: TypeAlias = Annotated[
    Union[BetaAWSExternalStorageConfig, BetaGCPExternalStorageConfig], UnionDiscriminator("type")
]

Status: TypeAlias = Annotated[
    Union[
        BetaPendingConfigurationExternalStorageStatus,
        BetaAvailableExternalStorageStatus,
        BetaActiveExternalStorageStatus,
        BetaDrainingExternalStorageStatus,
    ],
    UnionDiscriminator("type"),
]


class BetaExternalStorage(BaseModel):
    """A storage bucket in the organization's own cloud account.

    Anthropic writes
    inference data to it from each Workspace it is attached to.
    """

    id: str
    """The External Storage ID, which starts with `estrg_`.

    Through Claude Platform on AWS, storage whose `provider_config.type` is `aws`
    has its bucket ARN as its ID instead: `arn:<partition>:s3:::<bucket_name>`,
    where `<partition>` is the partition of the bucket's region.
    """

    created_at: datetime

    display_name: Optional[str] = None
    """Human-friendly display name. Null if none was set."""

    provider_config: ProviderConfig

    setup_template_version: Optional[str] = None
    """
    The version of Anthropic's setup template whose IAM role names this storage was
    found to use at activation. Null if no version was recorded, as for storage not
    yet activated or not on S3.
    """

    status: Status

    type: Literal["external_storage"]

    updated_at: datetime

    user_profile_id: Optional[str] = None
    """The user profile the storage is bound to, or null."""
