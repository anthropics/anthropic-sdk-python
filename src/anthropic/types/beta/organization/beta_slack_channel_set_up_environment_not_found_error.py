from typing_extensions import Literal

from ...._exceptions import NotFoundError
from .beta_slack_channel_set_up_environment_not_found_error_details import (
    BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails,
)

__all__ = ["BetaSlackChannelSetUpEnvironmentNotFoundError"]


class BetaSlackChannelSetUpEnvironmentNotFoundError(NotFoundError):
    """
    `settings.environment_id` names no Environment within the organization's reach, and the request had set the channel up by then. The channel stays set up with every setting unset.
    """

    error_code: Literal["slack_channel_set_up_environment_not_found"]  # pyright: ignore[reportIncompatibleVariableOverride]
    details: BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails  # pyright: ignore[reportIncompatibleVariableOverride]
