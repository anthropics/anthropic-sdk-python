from typing import Union
from typing_extensions import Annotated, TypeAlias

from ....._models import UnionDiscriminator
from .beta_compliance_review_content_not_captured import BetaComplianceReviewContentNotCaptured
from .beta_compliance_review_stored_copy_unavailable import BetaComplianceReviewStoredCopyUnavailable

__all__ = ["BetaComplianceReviewContentUnavailableReason"]

BetaComplianceReviewContentUnavailableReason: TypeAlias = Annotated[
    Union[BetaComplianceReviewContentNotCaptured, BetaComplianceReviewStoredCopyUnavailable], UnionDiscriminator("type")
]
"""Why a message's content isn't returned."""
