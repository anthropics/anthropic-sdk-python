from __future__ import annotations

from typing import List
from typing_extensions import Required, TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["SlackChannelListParams"]


class SlackChannelListParams(TypedDict, total=False):
    slack_workspace_id: Required[str]
    """
    The Slack workspace whose channels to list: Slack's identifier for it, as in the
    channel object's `slack.workspace_id`, not the workspace object's `id`.
    """

    include_inherited: bool
    """
    When `true`, `settings` holds what applies in each channel once the settings
    levels above it are taken into account, and every member of `sources` names the
    level a value comes from. When `false` or left out, `settings` holds what each
    channel itself stores.
    """

    limit: int
    """Number of items to return per page, between 1 and 100. Defaults to 20."""

    page: str
    """Opaque cursor from a previous response's `next_page`."""

    slack_channel_id: str
    """
    Slack's identifier for one channel of that workspace, as in the channel object's
    `slack.channel_id`. It is not the channel object's `id`. With it `data` holds
    that channel alone, or nothing when the channel is not set up.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
