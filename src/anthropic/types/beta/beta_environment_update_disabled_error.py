from typing_extensions import Literal

from ..._exceptions import PermissionDeniedError
from .beta_environment_update_disabled_error_details import BetaEnvironmentUpdateDisabledErrorDetails

__all__ = ["BetaEnvironmentUpdateDisabledError"]


class BetaEnvironmentUpdateDisabledError(PermissionDeniedError):
    """Anthropic has turned off updating environments for this organization.

    Existing environments still work as they are.
    """

    error_code: Literal["environment_update_disabled"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaEnvironmentUpdateDisabledErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
