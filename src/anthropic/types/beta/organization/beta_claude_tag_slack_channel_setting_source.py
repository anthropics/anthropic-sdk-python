from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagSlackChannelSettingSource"]


class BetaClaudeTagSlackChannelSettingSource(BaseModel):
    """The value comes from the addressed Slack channel itself."""

    slack_channel_id: str
    """The channel's identifier, starting with `slch_`."""

    type: Literal["slack_channel"]
