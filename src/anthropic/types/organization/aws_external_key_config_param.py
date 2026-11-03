from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AWSExternalKeyConfigParam"]


class AWSExternalKeyConfigParam(TypedDict, total=False):
    kms_arn: Required[str]
    """Full ARN of the AWS KMS key.

    On Claude Platform on AWS, alias ARNs are rejected, and your organization's own
    key must be a single-Region key in your organization's AWS account.
    """

    type: Required[Literal["aws"]]

    region: Optional[str]
    """AWS region. Derived from `kms_arn` if omitted."""
