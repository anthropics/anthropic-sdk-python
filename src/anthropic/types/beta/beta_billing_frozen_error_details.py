from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaBillingFrozenErrorDetails"]


class BetaBillingFrozenErrorDetails(BaseModel):
    """
    Anthropic has temporarily disabled billing changes for the user account the credential belongs to. Contact support.
    """

    error_code: Literal["billing_frozen"]
