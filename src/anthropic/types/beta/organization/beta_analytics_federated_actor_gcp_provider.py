from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsFederatedActorGCPProvider"]


class BetaAnalyticsFederatedActorGCPProvider(BaseModel):
    project_number: str
    """The Google Cloud project the organization is bound to."""

    type: Literal["gcp"]
