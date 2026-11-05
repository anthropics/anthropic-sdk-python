from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails"]


class BetaSlackChannelSetUpEnvironmentNotFoundErrorDetails(BaseModel):
    """
    `settings.environment_id` names no Environment within the organization's reach, and the request had set the channel up by then. The channel stays set up with every setting unset.
    """

    error_code: Literal["slack_channel_set_up_environment_not_found"]

    slack_channel_id: str
    """The identifier of the channel the request set up, starting with `slch_`."""
