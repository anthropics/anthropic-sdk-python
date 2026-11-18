from typing_extensions import Literal

from ...._exceptions import ConflictError
from .beta_slack_channel_set_up_settings_conflict_error_details import BetaSlackChannelSetUpSettingsConflictErrorDetails

__all__ = ["BetaSlackChannelSetUpSettingsConflictError"]


class BetaSlackChannelSetUpSettingsConflictError(ConflictError):
    """
    The request set the channel up, and something else then changed the channel or removed it. Nothing of `settings` was stored.
    """

    error_code: Literal["slack_channel_set_up_settings_conflict"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSlackChannelSetUpSettingsConflictErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
