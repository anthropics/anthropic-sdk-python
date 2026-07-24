# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from ..._models import BaseModel
from .beta_fallback_credit_redeemed import BetaFallbackCreditRedeemed
from .beta_fallback_credit_not_applied import BetaFallbackCreditNotApplied

__all__ = ["BetaFallbackCreditUsage", "Status"]

Status: TypeAlias = Annotated[
    Union[BetaFallbackCreditRedeemed, BetaFallbackCreditNotApplied], PropertyInfo(discriminator="type")
]


class BetaFallbackCreditUsage(BaseModel):
    """Outcome of the ``fallback_credit_token`` presented on this request."""

    status: Status
    """Whether the fallback-credit reprice was applied to this response's billing.

    A union discriminated on `type`. `redeemed`: the retry is billed as if the
    conversation had been on the retry model all along — including when the
    resulting shift is zero because there was nothing to move. `not_applied`: no
    reprice was applied; the arm's `reason` says why.
    """
