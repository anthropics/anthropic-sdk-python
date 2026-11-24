from typing_extensions import Literal

from ....._models import BaseModel
from .beta_compliance_review_case_close_reason import BetaComplianceReviewCaseCloseReason

__all__ = ["BetaComplianceReviewCaseClosed"]


class BetaComplianceReviewCaseClosed(BaseModel):
    """Anthropic has stopped waiting for a response. A closed case stays closed."""

    reason: BetaComplianceReviewCaseCloseReason
    """Why the case closed. It doesn't change afterwards."""

    type: Literal["closed"]
