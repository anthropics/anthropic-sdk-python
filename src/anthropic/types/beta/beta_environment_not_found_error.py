from typing_extensions import Literal

from ..._exceptions import NotFoundError
from .beta_environment_not_found_error_details import BetaEnvironmentNotFoundErrorDetails

__all__ = ["BetaEnvironmentNotFoundError"]


class BetaEnvironmentNotFoundError(NotFoundError):
    """`settings.environment_id` names no Environment within the organization's reach."""

    error_code: Literal["environment_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaEnvironmentNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
