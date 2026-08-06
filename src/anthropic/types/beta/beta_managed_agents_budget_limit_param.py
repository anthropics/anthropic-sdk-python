# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from ..beta_monetary_amount_param import BetaMonetaryAmountParam

__all__ = ["BetaManagedAgentsBudgetLimitParam"]


class BetaManagedAgentsBudgetLimitParam(TypedDict, total=False):
    """A hard spend ceiling.

    The session stops issuing new model requests once the tracked list cost reaches `max_list_cost`.
    """

    max_list_cost: Required[BetaMonetaryAmountParam]
    """A monetary amount in a specific currency."""

    type: Required[Literal["limit"]]
