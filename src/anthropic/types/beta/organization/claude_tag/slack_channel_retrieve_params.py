from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["SlackChannelRetrieveParams"]


class SlackChannelRetrieveParams(TypedDict, total=False):
    include_inherited: bool
    """
    When `true`, `settings` holds what applies in the channel once the settings
    levels above it are taken into account, and every member of `sources` names the
    level a value comes from. When `false` or left out, `settings` holds what the
    channel itself stores.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
