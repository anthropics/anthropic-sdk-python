from ...._models import BaseModel

__all__ = ["BetaClaudeTagSlackChannelIdentifiers"]


class BetaClaudeTagSlackChannelIdentifiers(BaseModel):
    """The identifiers Slack shows for a channel.

    They are Slack's own, not identifiers of this API.
    """

    channel_id: str
    """
    Slack's identifier for the channel, starting with `C` or `G`, such as
    `C0456EFGH`.
    """

    workspace_id: str
    """
    Slack's identifier for the workspace the channel is in, starting with `T`, such
    as `T0123ABCD`.
    """
