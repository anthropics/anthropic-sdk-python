from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAWSExternalKeyConfig"]


class BetaAWSExternalKeyConfig(BaseModel):
    kms_arn: str
    """Full ARN of the AWS KMS key.

    On Claude Platform on AWS, alias ARNs are rejected, and your organization's own
    key must be a single-Region key in your organization's AWS account.
    """

    type: Literal["aws"]

    region: Optional[str] = None
    """AWS region. Derived from `kms_arn` if omitted."""

    role_arn: Optional[str] = None
    """IAM role ARN. Deprecated; this field is ignored."""
