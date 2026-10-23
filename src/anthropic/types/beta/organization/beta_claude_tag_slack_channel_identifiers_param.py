from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["BetaClaudeTagSlackChannelIdentifiersParam"]


class BetaClaudeTagSlackChannelIdentifiersParam(TypedDict, total=False):
    """The identifiers Slack shows for a channel.

    They are Slack's own, not identifiers of this API.
    """

    channel_id: Required[str]
    """
    Slack's identifier for the channel, starting with `C` or `G`, such as
    `C0456EFGH`.
    """

    workspace_id: Required[str]
    """
    Slack's identifier for the workspace the channel is in, starting with `T`, such
    as `T0123ABCD`.
    """
