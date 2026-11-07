from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeTagSlackChannelBundleTarget"]


class BetaClaudeTagSlackChannelBundleTarget(BaseModel):
    """One Bundle attached to one Slack channel.

    The Bundle can be used in that channel only.
    """

    id: str
    """The Bundle Target's identifier.

    Starts with `btgt_`. No two Bundle Targets have the same one, and the same
    Bundle and target always give the same one, also after a detach and a new
    attach. It is opaque.
    """

    created_at: datetime
    """Time the Bundle was attached."""

    slack_channel_id: str
    """
    The identifier of the Slack channel the Bundle is attached to, starting with
    `slch_`. It is the channel object's `id`, not Slack's `channel_id`.
    """

    type: Literal["slack_channel"]
