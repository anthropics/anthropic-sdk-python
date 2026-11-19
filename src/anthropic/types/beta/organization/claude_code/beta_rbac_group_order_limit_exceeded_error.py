from typing_extensions import Literal

from ....._exceptions import BadRequestError
from .beta_rbac_group_order_limit_exceeded_error_details import BetaRBACGroupOrderLimitExceededErrorDetails

__all__ = ["BetaRBACGroupOrderLimitExceededError"]


class BetaRBACGroupOrderLimitExceededError(BadRequestError):
    """The RBAC Group order already has the most groups allowed.

    Delete another group's settings first.
    """

    error_code: Literal["rbac_group_order_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaRBACGroupOrderLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
