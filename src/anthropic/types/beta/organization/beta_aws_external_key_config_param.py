# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaAWSExternalKeyConfigParam"]


class BetaAWSExternalKeyConfigParam(TypedDict, total=False):
    kms_arn: Required[str]
    """Full ARN of the AWS KMS key.

    On Claude Platform on AWS the key must be a single-Region key in your
    organization's own AWS account; cross-account keys, multi-Region keys, and alias
    ARNs are rejected.
    """

    type: Required[Literal["aws"]]

    region: Optional[str]
    """AWS region. Derived from `kms_arn` if omitted."""

    role_arn: Optional[str]
    """IAM role ARN.

    Deprecated — Anthropic reaches the KMS key through its own intermediate role
    (or, on Claude Platform on AWS, with credentials AWS issues for the Workspace);
    this field is ignored.
    """
