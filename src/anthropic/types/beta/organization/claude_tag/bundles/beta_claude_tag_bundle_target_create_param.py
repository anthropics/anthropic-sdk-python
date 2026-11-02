from __future__ import annotations

from typing import Union
from typing_extensions import TypeAlias

from .beta_claude_tag_slack_channel_bundle_target_create_param import BetaClaudeTagSlackChannelBundleTargetCreateParam
from .beta_claude_tag_slack_workspace_bundle_target_create_param import (
    BetaClaudeTagSlackWorkspaceBundleTargetCreateParam,
)

__all__ = ["BetaClaudeTagBundleTargetCreateParam"]

BetaClaudeTagBundleTargetCreateParam: TypeAlias = Union[
    BetaClaudeTagSlackChannelBundleTargetCreateParam, BetaClaudeTagSlackWorkspaceBundleTargetCreateParam
]
