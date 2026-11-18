from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSlackChannelSetUpSettingsRefusedErrorDetails"]


class BetaSlackChannelSetUpSettingsRefusedErrorDetails(BaseModel):
    """The request set the channel up, and `settings` was then refused.

    The channel stays set up with every setting unset.
    """

    error_code: Literal["slack_channel_set_up_settings_refused"]
    """A stable code that names the cause."""

    slack_channel_id: str
    """The identifier of the channel the request set up, starting with `slch_`."""
