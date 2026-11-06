from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaManagedAgentsAWSRoleExecutionIdentity"]


class BetaManagedAgentsAWSRoleExecutionIdentity(BaseModel):
    """An AWS IAM role principal as returned in API responses."""

    role_arn: str
    """The IAM role's ARN."""

    type: Literal["aws_role"]
