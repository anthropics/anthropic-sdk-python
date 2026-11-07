from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsFederatedActorAzureProvider"]


class BetaAnalyticsFederatedActorAzureProvider(BaseModel):
    subscription_id: str
    """The Azure subscription the organization is bound to."""

    type: Literal["azure"]
