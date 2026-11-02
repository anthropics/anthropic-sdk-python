from datetime import datetime
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["BetaClaudeTagSlackWorkspaceBundleTarget"]


class BetaClaudeTagSlackWorkspaceBundleTarget(BaseModel):
    """One Bundle attached to one Slack workspace.

    The Bundle can be used in the workspace and in every channel in it.
    """

    id: str
    """The Bundle Target's identifier.

    Starts with `btgt_`. No two Bundle Targets have the same one, and the same
    Bundle and target always give the same one, also after a detach and a new
    attach. It is opaque.
    """

    created_at: datetime
    """Time the Bundle was attached."""

    slack_workspace_id: str
    """
    The identifier of the Slack workspace the Bundle is attached to, starting with
    `slws_`.
    """

    type: Literal["slack_workspace"]
