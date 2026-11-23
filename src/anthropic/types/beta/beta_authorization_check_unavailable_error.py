from typing_extensions import Literal

from ..._exceptions import ServiceUnavailableError
from .beta_authorization_check_unavailable_error_details import BetaAuthorizationCheckUnavailableErrorDetails

__all__ = ["BetaAuthorizationCheckUnavailableError"]


class BetaAuthorizationCheckUnavailableError(ServiceUnavailableError):
    """
    One of the organization's approvals from Anthropic could not be read right now, so nothing was done. Retry after the `Retry-After` delay.
    """

    error_code: Literal["authorization_check_unavailable"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaAuthorizationCheckUnavailableErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
