from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsFederatedActorAWSProvider"]


class BetaAnalyticsFederatedActorAWSProvider(BaseModel):
    account_id: str
    """The AWS account the organization is bound to."""

    signed_principal: str
    """The AWS-signed ARN of the IAM principal that made the requests."""

    type: Literal["aws"]
