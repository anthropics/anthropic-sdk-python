from typing_extensions import Literal

from ...._exceptions import BadRequestError
from .beta_slack_channel_set_up_settings_refused_error_details import BetaSlackChannelSetUpSettingsRefusedErrorDetails

__all__ = ["BetaSlackChannelSetUpSettingsRefusedError"]


class BetaSlackChannelSetUpSettingsRefusedError(BadRequestError):
    """The request set the channel up, and `settings` was then refused.

    The channel stays set up with every setting unset.
    """

    error_code: Literal["slack_channel_set_up_settings_refused"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSlackChannelSetUpSettingsRefusedErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
