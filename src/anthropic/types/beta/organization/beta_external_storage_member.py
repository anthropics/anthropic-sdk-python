from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaExternalStorageMember"]


class BetaExternalStorageMember(BaseModel):
    """The organization's External Storage that `external_storage_id` names."""

    external_storage_id: str
    """The External Storage ID, which starts with `estrg_`.

    Through Claude Platform on AWS, storage whose `provider_config.type` is `aws`
    has its bucket ARN as its ID instead: `arn:<partition>:s3:::<bucket_name>`,
    where `<partition>` is the partition of the bucket's region.
    """

    type: Literal["external"]
