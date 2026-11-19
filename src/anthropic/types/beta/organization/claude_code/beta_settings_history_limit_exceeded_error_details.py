from typing_extensions import Literal

from ....._models import BaseModel

__all__ = ["BetaSettingsHistoryLimitExceededErrorDetails"]


class BetaSettingsHistoryLimitExceededErrorDetails(BaseModel):
    """
    The organization has reached its settings history limit, a cap on stored versions of its settings documents. Nothing in the API or claude.ai lowers the count, so contact support. Creating or deleting group settings, creating or clearing the default settings, and reordering are refused. Changing the mode still works, unless it would copy the organization settings into a new default.
    """

    error_code: Literal["settings_history_limit_exceeded"]
