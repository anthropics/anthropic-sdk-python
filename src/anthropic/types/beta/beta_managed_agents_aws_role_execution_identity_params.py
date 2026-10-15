from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaManagedAgentsAWSRoleExecutionIdentityParams"]


class BetaManagedAgentsAWSRoleExecutionIdentityParams(TypedDict, total=False):
    """An AWS IAM role principal."""

    role_arn: Required[str]
    """The IAM role's ARN, e.g.

    "arn:aws:iam::123456789012:role/my-agent-runner". Maximum 2048 characters.
    """

    type: Required[Literal["aws_role"]]
