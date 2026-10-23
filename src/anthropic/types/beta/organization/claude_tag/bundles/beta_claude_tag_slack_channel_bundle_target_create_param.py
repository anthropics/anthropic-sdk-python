from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagSlackChannelBundleTargetCreateParam"]


class BetaClaudeTagSlackChannelBundleTargetCreateParam(TypedDict, total=False):
    """Attach the Bundle to a Slack channel."""

    slack_channel_id: Required[str]
    """
    The identifier of the Slack channel to attach the Bundle to, starting with
    `slch_`. It is the channel object's `id`, not Slack's `channel_id`.
    """

    type: Required[Literal["slack_channel"]]
