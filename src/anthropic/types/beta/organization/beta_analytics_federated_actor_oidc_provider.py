from typing import Optional
from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsFederatedActorOIDCProvider"]


class BetaAnalyticsFederatedActorOIDCProvider(BaseModel):
    issuer: Optional[str] = None
    """The federation issuer's URL."""

    type: Literal["oidc"]
