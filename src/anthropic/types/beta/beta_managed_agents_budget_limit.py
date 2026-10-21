from typing_extensions import Literal

from ..._models import BaseModel
from ..beta_monetary_amount import BetaMonetaryAmount

__all__ = ["BetaManagedAgentsBudgetLimit"]


class BetaManagedAgentsBudgetLimit(BaseModel):
    """A hard spend ceiling.

    The session stops issuing new model requests once the tracked list cost reaches `max_list_cost`.
    """

    max_list_cost: BetaMonetaryAmount
    """Maximum list cost the session may accrue.

    List price is used regardless of any negotiated discount, so the cap fires at or
    before the actual charge.
    """

    type: Literal["limit"]
