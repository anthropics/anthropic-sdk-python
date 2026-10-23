from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel
from .beta_analytics_federated_actor_provider import BetaAnalyticsFederatedActorProvider

__all__ = ["BetaAnalyticsFederatedActor"]


class BetaAnalyticsFederatedActor(BaseModel):
    provider: BetaAnalyticsFederatedActorProvider
    """The trusted provider that asserted the caller's identity."""

    subject: Optional[str] = None
    """
    The provider's identifier for the caller: on `aws`, the IAM principal ARN (one
    role is one actor across its sessions); on `gcp`, the caller's IAM principal
    identifier as Google Cloud reports it, such as `serviceAccount:<email>`,
    `user:<email>`, or a `principal://...` URI.
    """

    type: Literal["federated_actor"]
