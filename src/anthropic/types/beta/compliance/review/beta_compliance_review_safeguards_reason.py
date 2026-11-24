from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaComplianceReviewSafeguardsReason"]


class BetaComplianceReviewSafeguardsReason(BaseModel):
    """Anthropic flagged the item for your organization to review."""

    type: Literal["safeguards_review"]
