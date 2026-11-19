from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaRBACGroupOrderLimitExceededErrorDetails"]


class BetaRBACGroupOrderLimitExceededErrorDetails(BaseModel):
    """The RBAC Group order already has the most groups allowed.

    Delete another group's settings first.
    """

    error_code: Literal["rbac_group_order_limit_exceeded"]
