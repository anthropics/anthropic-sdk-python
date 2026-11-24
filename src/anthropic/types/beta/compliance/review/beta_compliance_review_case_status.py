from typing import Union
from typing_extensions import Annotated, TypeAlias

from ....._models import UnionDiscriminator
from .beta_compliance_review_case_open import BetaComplianceReviewCaseOpen
from .beta_compliance_review_case_closed import BetaComplianceReviewCaseClosed

__all__ = ["BetaComplianceReviewCaseStatus"]

BetaComplianceReviewCaseStatus: TypeAlias = Annotated[
    Union[BetaComplianceReviewCaseOpen, BetaComplianceReviewCaseClosed], UnionDiscriminator("type")
]
"""The status of a review case."""
