from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewContentNotCaptured"]


class BetaComplianceReviewContentNotCaptured(BaseModel):
    """No copy of the message was stored."""

    type: Literal["not_captured"]
