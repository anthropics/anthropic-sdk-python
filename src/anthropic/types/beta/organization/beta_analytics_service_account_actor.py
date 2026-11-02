from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaAnalyticsServiceAccountActor"]


class BetaAnalyticsServiceAccountActor(BaseModel):
    service_account_id: str
    """Tagged service account ID."""

    type: Literal["service_account_actor"]
