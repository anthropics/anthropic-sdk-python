from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

from ....anthropic_beta_param import AnthropicBetaParam

__all__ = ["SlackWorkspaceListParams"]


class SlackWorkspaceListParams(TypedDict, total=False):
    include_inherited: bool
    """
    When `true`, `settings` holds what applies in each workspace once the
    organization's Slack defaults are taken into account, and every member of
    `sources` names the level a value comes from. When `false` or left out,
    `settings` holds what each workspace itself stores.
    """

    limit: int
    """Number of items to return per page, between 1 and 100. Defaults to 20."""

    page: str
    """Opaque cursor from a previous response's `next_page`."""

    slack_workspace_id: str
    """
    Slack's identifier for one workspace, as in the workspace object's
    `slack.workspace_id`, not its `id`. With it `data` holds that workspace alone,
    or nothing when it is not set up.
    """

    betas: List[AnthropicBetaParam]
    """
    This endpoint is in beta: requests must send
    `experimental-claude-tag-2026-10-21` in this header.
    """
