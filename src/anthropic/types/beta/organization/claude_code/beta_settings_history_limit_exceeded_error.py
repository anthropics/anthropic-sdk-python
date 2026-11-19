from typing_extensions import Literal

from ....._exceptions import BadRequestError
from .beta_settings_history_limit_exceeded_error_details import BetaSettingsHistoryLimitExceededErrorDetails

__all__ = ["BetaSettingsHistoryLimitExceededError"]


class BetaSettingsHistoryLimitExceededError(BadRequestError):
    """
    The organization has reached its settings history limit, a cap on stored versions of its settings documents. Nothing in the API or claude.ai lowers the count, so contact support. Creating or deleting group settings, creating or clearing the default settings, and reordering are refused. Changing the mode still works, unless it would copy the organization settings into a new default.
    """

    error_code: Literal["settings_history_limit_exceeded"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSettingsHistoryLimitExceededErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
