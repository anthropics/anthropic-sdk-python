from typing import Union, Optional
from datetime import datetime
from typing_extensions import Literal, Annotated, TypeAlias

from ...._models import BaseModel, UnionDiscriminator
from .beta_spend_limit_period import BetaSpendLimitPeriod
from .beta_spend_limit_user_scope import BetaSpendLimitUserScope
from .beta_spend_limit_seat_tier_scope import BetaSpendLimitSeatTierScope
from .beta_spend_limit_workspace_scope import BetaSpendLimitWorkspaceScope
from .beta_spend_limit_rbac_group_scope import BetaSpendLimitRBACGroupScope
from .beta_spend_limit_organization_scope import BetaSpendLimitOrganizationScope
from .beta_spend_limit_organization_service_scope import BetaSpendLimitOrganizationServiceScope

__all__ = ["BetaSpendLimit", "Scope"]

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


class BetaSpendLimit(BaseModel):
    """A configured spend limit: a cap on metered spend for one scope and period."""

    id: str
    """Unique tagged ID of the spend limit (`spl_...`)."""

    amount: Optional[str] = None
    """
    Limit amount as a non-negative integer decimal string in the minor unit of
    `currency` (cents for USD): "50000" is $500.00. `null` means no numeric cap is
    configured at this scope — see the effective report for whether a limit applies.
    """

    created_at: datetime
    """RFC 3339 datetime at which the spend limit was created."""

    currency: str
    """ISO 4217 code of the organization's billing currency; the unit for `amount`."""

    is_enabled: bool
    """Read-only.

    `false` when extra usage is switched off for this organization (`organization`
    limit) or for this member (`user` limit); `amount` is kept and applies again
    when it's switched back on. Always `true` for other limits.
    """

    period: BetaSpendLimitPeriod
    """Length of the window the limit resets over.

    `amount` caps spend within each period.
    """

    scope: Scope
    """What the limit applies to.

    A tagged union on `type`; each variant carries the identifier for its scope.
    """

    type: Literal["spend_limit"]
    """Object type. Always `spend_limit`."""

    updated_at: datetime
    """RFC 3339 datetime at which the spend limit was last modified."""
