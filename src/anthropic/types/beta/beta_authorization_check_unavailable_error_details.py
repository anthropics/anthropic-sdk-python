from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["BetaAuthorizationCheckUnavailableErrorDetails"]


class BetaAuthorizationCheckUnavailableErrorDetails(BaseModel):
    """
    One of the organization's approvals from Anthropic could not be read right now, so nothing was done. Retry after the `Retry-After` delay.
    """

    error_code: Literal["authorization_check_unavailable"]
