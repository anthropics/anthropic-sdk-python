from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["SlackWorkspaceRetrieveParams"]


class SlackWorkspaceRetrieveParams(TypedDict, total=False):
    include_inherited: bool
    """
    When `true`, `settings` holds what applies in the workspace once the
    organization's Slack defaults are taken into account, and every member of
    `sources` names the level a value comes from. When `false` or left out,
    `settings` holds what the workspace itself stores.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
