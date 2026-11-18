from typing_extensions import Literal

from ..._exceptions import BadRequestError
from .beta_environment_archived_error_details import BetaEnvironmentArchivedErrorDetails

__all__ = ["BetaEnvironmentArchivedError"]


class BetaEnvironmentArchivedError(BadRequestError):
    """The environment is archived, so it cannot be updated."""

    error_code: Literal["environment_archived"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaEnvironmentArchivedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
