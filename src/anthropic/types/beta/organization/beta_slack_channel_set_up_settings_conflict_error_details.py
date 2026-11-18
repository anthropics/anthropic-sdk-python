from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaSlackChannelSetUpSettingsConflictErrorDetails"]


class BetaSlackChannelSetUpSettingsConflictErrorDetails(BaseModel):
    """
    The request set the channel up, and something else then changed the channel or removed it. Nothing of `settings` was stored.
    """

    error_code: Literal["slack_channel_set_up_settings_conflict"]
    """A stable code that names the cause."""

    slack_channel_id: str
    """The identifier of the channel the request set up, starting with `slch_`."""
