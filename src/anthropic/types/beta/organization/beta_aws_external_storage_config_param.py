from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaAWSExternalStorageConfigParam"]


class BetaAWSExternalStorageConfigParam(TypedDict, total=False):
    """An Amazon S3 bucket."""

    account_id: Required[str]
    """12-digit ID of the AWS account that owns the bucket."""

    bucket_name: Required[str]
    """
    The bucket's name, without `s3://`: 3 to 63 lower-case letters, digits and
    hyphens, starting and ending with a letter or digit.
    """

    region: Required[str]
    """The bucket's AWS region.

    Activating the storage fails if Anthropic can't use buckets in that region.
    """

    type: Required[Literal["aws"]]
