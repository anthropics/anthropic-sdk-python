from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["BetaClaudeTagSlackWorkspaceBundleTargetCreateParam"]


class BetaClaudeTagSlackWorkspaceBundleTargetCreateParam(TypedDict, total=False):
    """Attach the Bundle to a Slack workspace."""

    slack_workspace_id: Required[str]
    """
    The identifier of the Slack workspace to attach the Bundle to, starting with
    `slws_`.
    """

    type: Required[Literal["slack_workspace"]]
