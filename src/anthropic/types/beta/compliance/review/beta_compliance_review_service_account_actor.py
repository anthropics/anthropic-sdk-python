from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewServiceAccountActor"]


class BetaComplianceReviewServiceAccountActor(BaseModel):
    """A service account."""

    service_account_id: str
    """The ID of the service account (`svac_...`)."""

    type: Literal["service_account_actor"]
