from typing import Union
from typing_extensions import Annotated, TypeAlias

from ....._models import UnionDiscriminator
from .beta_compliance_review_api_actor import BetaComplianceReviewAPIActor
from .beta_compliance_review_user_actor import BetaComplianceReviewUserActor
from .beta_compliance_review_service_account_actor import BetaComplianceReviewServiceAccountActor

__all__ = ["BetaComplianceReviewActor"]

BetaComplianceReviewActor: TypeAlias = Annotated[
    Union[BetaComplianceReviewUserActor, BetaComplianceReviewAPIActor, BetaComplianceReviewServiceAccountActor],
    UnionDiscriminator("type"),
]
"""Who sent a message."""
