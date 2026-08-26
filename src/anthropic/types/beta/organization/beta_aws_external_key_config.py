# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAWSExternalKeyConfig"]


class BetaAWSExternalKeyConfig(BaseModel):
    kms_arn: str
    """Full ARN of the AWS KMS key."""

    type: Literal["aws"]

    region: Optional[str] = None
    """AWS region. Derived from `kms_arn` if omitted."""

    role_arn: Optional[str] = None
    """IAM role ARN.

    Deprecated — Anthropic reaches the KMS key via a managed intermediate role; this
    field is ignored.
    """
