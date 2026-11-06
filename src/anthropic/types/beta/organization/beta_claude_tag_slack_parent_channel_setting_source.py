from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagSlackParentChannelSettingSource"]


class BetaClaudeTagSlackParentChannelSettingSource(BaseModel):
    """The value comes from the channel that a code channel was started from.

    A parent channel contributes `instructions` and `environment_id` only.
    """

    slack_channel_id: str
    """The parent channel's identifier, starting with `slch_`."""

    type: Literal["slack_parent_channel"]
