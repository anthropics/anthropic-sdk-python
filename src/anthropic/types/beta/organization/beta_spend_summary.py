from typing import Union, Optional
from typing_extensions import Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_spend_limit_period import BetaSpendLimitPeriod
from .beta_spend_limit_user_actor import BetaSpendLimitUserActor
from .beta_spend_limit_user_scope import BetaSpendLimitUserScope
from .beta_spend_limit_seat_tier_scope import BetaSpendLimitSeatTierScope
from .beta_spend_limit_workspace_scope import BetaSpendLimitWorkspaceScope
from .beta_spend_limit_rbac_group_scope import BetaSpendLimitRBACGroupScope
from .beta_spend_limit_organization_scope import BetaSpendLimitOrganizationScope
from .beta_spend_limit_scoped_api_key_actor import BetaSpendLimitScopedAPIKeyActor
from .beta_spend_limit_organization_service_scope import BetaSpendLimitOrganizationServiceScope

__all__ = ["BetaSpendSummary", "Actor", "Scope", "Source"]

Actor: TypeAlias = Annotated[
    Union[BetaSpendLimitUserActor, BetaSpendLimitScopedAPIKeyActor], UnionDiscriminator("type")
]

Scope: TypeAlias = Annotated[
    Union[
        BetaSpendLimitUserScope,
        BetaSpendLimitSeatTierScope,
        BetaSpendLimitRBACGroupScope,
        BetaSpendLimitOrganizationServiceScope,
        BetaSpendLimitOrganizationScope,
        BetaSpendLimitWorkspaceScope,
    ],
    UnionDiscriminator("type"),
]

Source: TypeAlias = Annotated[
    Union[
        BetaSpendLimitUserScope,
        BetaSpendLimitSeatTierScope,
        BetaSpendLimitRBACGroupScope,
        BetaSpendLimitOrganizationServiceScope,
        BetaSpendLimitOrganizationScope,
        BetaSpendLimitWorkspaceScope,
    ],
    UnionDiscriminator("type"),
]


class BetaSpendSummary(BaseModel):
    """Per-member effective-limit report row (`GET /spend_limits/effective`)."""

    actor: Actor

    amount: Optional[str] = None
    """
    Effective limit amount as a non-negative integer decimal string in the minor
    unit of `currency` (cents for USD). `null` means no limit applies for this row's
    `period` — each period resolves independently, so another period may still cap
    this member.
    """

    currency: str
    """
    ISO 4217 code of the organization's billing currency; the unit for `amount` and
    `period_to_date_spend`.
    """

    period: BetaSpendLimitPeriod
    """Period this row's effective limit and spend are reported for."""

    period_to_date_spend: str
    """
    The member's spend so far in the current period, as a non-negative decimal
    string in the minor unit of `currency` (cents for USD). May carry fractional
    minor units up to three decimal places (e.g. `"12050.5"`) — metered usage is not
    rounded to whole cents. Reads as `"0"` when the spend reading is temporarily
    unavailable.
    """

    scope: Scope

    source: Source

    spend_limit_id: str
