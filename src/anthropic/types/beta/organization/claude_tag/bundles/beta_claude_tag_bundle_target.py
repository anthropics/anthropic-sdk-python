from typing import Union
from typing_extensions import Annotated, TypeAlias

from ......_models import UnionDiscriminator
from .beta_claude_tag_slack_channel_bundle_target import BetaClaudeTagSlackChannelBundleTarget
from .beta_claude_tag_slack_workspace_bundle_target import BetaClaudeTagSlackWorkspaceBundleTarget

__all__ = ["BetaClaudeTagBundleTarget"]

BetaClaudeTagBundleTarget: TypeAlias = Annotated[
    Union[BetaClaudeTagSlackChannelBundleTarget, BetaClaudeTagSlackWorkspaceBundleTarget], UnionDiscriminator("type")
]
"""One Bundle attached to one Slack channel or one Slack workspace.

More types of target can be added.
"""
