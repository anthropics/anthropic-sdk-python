from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ....._models import BaseModel, UnionDiscriminator
from ..beta_spend_limit import BetaSpendLimit
from ..beta_spend_summary import BetaSpendSummary
from ..beta_spend_limit_period import BetaSpendLimitPeriod
from ..beta_spend_limit_user_actor import BetaSpendLimitUserActor
from ..beta_spend_limit_scoped_api_key_actor import BetaSpendLimitScopedAPIKeyActor
from .beta_spend_limit_increase_request_status import BetaSpendLimitIncreaseRequestStatus

__all__ = ["IncreaseRequestApproveResponse", "Actor", "ResolvedBy"]

Actor: TypeAlias = Annotated[
    Union[BetaSpendLimitUserActor, BetaSpendLimitScopedAPIKeyActor], UnionDiscriminator("type")
]

ResolvedBy: TypeAlias = Annotated[
    Union[BetaSpendLimitUserActor, BetaSpendLimitScopedAPIKeyActor, None], UnionDiscriminator("type")
]


class IncreaseRequestApproveResponse(BaseModel):
    id: str

    actor: Actor

    created_at: datetime

    period: BetaSpendLimitPeriod

    resolved_at: Optional[datetime] = None

    resolved_by: Optional[ResolvedBy] = None

    spend_limit: BetaSpendLimit
    """A configured spend limit: a cap on metered spend for one scope and period."""

    spend_summary: Optional[BetaSpendSummary] = None
    """Per-member effective-limit report row (`GET /spend_limits/effective`)."""

    status: BetaSpendLimitIncreaseRequestStatus

    type: Literal["spend_limit_increase_request"]
