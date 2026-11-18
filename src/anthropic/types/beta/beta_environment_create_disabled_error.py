from typing_extensions import Literal

from ..._exceptions import PermissionDeniedError
from .beta_environment_create_disabled_error_details import BetaEnvironmentCreateDisabledErrorDetails

__all__ = ["BetaEnvironmentCreateDisabledError"]


class BetaEnvironmentCreateDisabledError(PermissionDeniedError):
    """Anthropic has turned off creating environments for this organization.

    Existing environments still work.
    """

    error_code: Literal["environment_create_disabled"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaEnvironmentCreateDisabledErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
