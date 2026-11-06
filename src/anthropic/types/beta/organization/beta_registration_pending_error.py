from typing_extensions import Literal

from ...._exceptions import ServiceUnavailableError
from .beta_registration_pending_error_details import BetaRegistrationPendingErrorDetails

__all__ = ["BetaRegistrationPendingError"]


class BetaRegistrationPendingError(ServiceUnavailableError):
    """The Plugin version was stored but is not yet usable in claude.ai.

    `plugin_id` and `plugin_version_id` identify what was stored.
    """

    error_code: Literal["registration_pending"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaRegistrationPendingErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
