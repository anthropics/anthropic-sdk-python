from typing_extensions import Literal

from ...._models import BaseModel

__all__ = ["BetaClaudeTagSlackWorkspaceSettingSource"]


class BetaClaudeTagSlackWorkspaceSettingSource(BaseModel):
    """The value comes from a Slack workspace of the organization."""

    slack_workspace_id: str
    """The workspace's identifier, starting with `slws_`."""

    type: Literal["slack_workspace"]
