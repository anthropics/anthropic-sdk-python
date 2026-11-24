from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .beta_compliance_review_determination import BetaComplianceReviewDetermination
from .beta_compliance_review_violated_policy_category import BetaComplianceReviewViolatedPolicyCategory

__all__ = ["BetaComplianceReviewVerdictParam"]


class BetaComplianceReviewVerdictParam(TypedDict, total=False):
    """Your conclusion on one message of a review case."""

    determination: Required[BetaComplianceReviewDetermination]
    """Your conclusion on this message."""

    item_id: Required[str]
    """The `item_id` of one of the case's `transcripts`."""

    policy_category: Optional[BetaComplianceReviewViolatedPolicyCategory]
    """
    The policy category that this message violated, from the values that the
    request's `policy_categories` accepts. Optional with `violation`. Leave it out
    with `no_violation`.
    """
