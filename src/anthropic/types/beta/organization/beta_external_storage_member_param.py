from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaExternalStorageMemberParam"]


class BetaExternalStorageMemberParam(TypedDict, total=False):
    """The organization's External Storage that `external_storage_id` names."""

    external_storage_id: Required[str]
    """The External Storage ID, which starts with `estrg_`.

    Through Claude Platform on AWS, storage whose `provider_config.type` is `aws`
    has its bucket ARN as its ID instead: `arn:<partition>:s3:::<bucket_name>`,
    where `<partition>` is the partition of the bucket's region.
    """

    type: Required[Literal["external"]]
