from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewCaseOpen"]


class BetaComplianceReviewCaseOpen(BaseModel):
    """Anthropic is waiting for a response to the case."""

    type: Literal["open"]
