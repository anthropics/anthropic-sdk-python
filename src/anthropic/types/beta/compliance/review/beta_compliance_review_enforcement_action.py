from ....._models import BaseModel

__all__ = ["BetaComplianceReviewEnforcementAction"]


class BetaComplianceReviewEnforcementAction(BaseModel):
    """An action that Anthropic took on the flagged traffic."""

    type: str
    """The kind of action.

    New values can appear, so accept a value that you don't know.
    """
