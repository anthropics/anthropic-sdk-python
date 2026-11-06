from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails"]


class BetaSpendLimitsAdminAPIWritesNotEnabledErrorDetails(BaseModel):
    """
    The organization cannot retrieve, set or delete spend limits with an Admin API credential.
    """

    error_code: Literal["spend_limits_admin_api_writes_not_enabled"]
