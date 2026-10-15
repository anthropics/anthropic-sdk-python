from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["AWSExternalKeyConfig"]


class AWSExternalKeyConfig(BaseModel):
    kms_arn: str
    """Full ARN of the AWS KMS key.

    On Claude Platform on AWS the key must be a single-Region key in your
    organization's own AWS account; cross-account keys, multi-Region keys, and alias
    ARNs are rejected.
    """

    type: Literal["aws"]

    region: Optional[str] = None
    """AWS region. Derived from `kms_arn` if omitted."""
