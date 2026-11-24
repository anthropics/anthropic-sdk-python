from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewAPIActor"]


class BetaComplianceReviewAPIActor(BaseModel):
    """An API key."""

    api_key_id: str
    """The ID of the API key (`apikey_...`)."""

    type: Literal["api_actor"]
