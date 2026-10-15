from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..beta_monetary_amount_param import BetaMonetaryAmountParam

__all__ = ["BetaManagedAgentsBudgetLimitParam"]


class BetaManagedAgentsBudgetLimitParam(TypedDict, total=False):
    """A hard spend ceiling.

    The session stops issuing new model requests once the tracked list cost reaches `max_list_cost`.
    """

    max_list_cost: Required[BetaMonetaryAmountParam]
    """Maximum list cost the session may accrue.

    List price is used regardless of any negotiated discount, so the cap fires at or
    before the actual charge.
    """

    type: Required[Literal["limit"]]
