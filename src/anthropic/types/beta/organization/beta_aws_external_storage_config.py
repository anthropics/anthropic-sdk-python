from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAWSExternalStorageConfig"]


class BetaAWSExternalStorageConfig(BaseModel):
    """An Amazon S3 bucket."""

    account_id: str
    """12-digit ID of the AWS account that owns the bucket."""

    bucket_name: str
    """The bucket's name, without `s3://`."""

    region: str
    """The bucket's AWS region."""

    type: Literal["aws"]
