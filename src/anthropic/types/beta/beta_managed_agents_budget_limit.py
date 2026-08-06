# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel
from ..beta_monetary_amount import BetaMonetaryAmount

__all__ = ["BetaManagedAgentsBudgetLimit"]


class BetaManagedAgentsBudgetLimit(BaseModel):
    """A hard spend ceiling.

    The session stops issuing new model requests once the tracked list cost reaches `max_list_cost`.
    """

    max_list_cost: BetaMonetaryAmount
    """A monetary amount in a specific currency."""

    type: Literal["limit"]
