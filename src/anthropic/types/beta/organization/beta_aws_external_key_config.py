# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAWSExternalKeyConfig"]


class BetaAWSExternalKeyConfig(BaseModel):
    kms_arn: str
    """Full ARN of the AWS KMS key.

    On Claude Platform on AWS the key must be a single-Region key in your
    organization's own AWS account; cross-account keys, multi-Region keys, and alias
    ARNs are rejected.
    """

    type: Literal["aws"]

    region: Optional[str] = None
    """AWS region. Derived from `kms_arn` if omitted."""

    role_arn: Optional[str] = None
    """IAM role ARN.

    Deprecated — Anthropic reaches the KMS key through its own intermediate role
    (or, on Claude Platform on AWS, with credentials AWS issues for the Workspace);
    this field is ignored.
    """
